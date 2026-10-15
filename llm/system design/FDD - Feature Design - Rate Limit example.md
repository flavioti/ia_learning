## 1. Context and Technical Motivation
- **Problem Statement:** As API traffic scales across microservices and external integrations, downstream services face risks from traffic surges, scraping bots, malicious abuse, cascading failures, and unexpected infrastructure cost spikes (particularly for LLM/AI inference endpoints and high-throughput data pipelines).
- **Current Limitations:** Existing controls rely on fragmented, local in-memory counters per service instance or lack multi-tenant tier differentiation (e.g., Free, Pro, Enterprise tiers, requests-per-second vs. token-based quotas).
- **Motivation:** Implement a centralized, distributed, low-latency rate-limiting layer at the API Gateway level backed by a Redis Cluster, utilizing sliding window counter and token bucket algorithms executed atomically via Lua scripts.
## 2. Technical Objectives
- **Sub-millisecond Overhead:** Maintain less than 2ms of p99 latency overhead for API request evaluation.
- **High Availability & Fault Tolerance:** Target 99.99% availability with graceful fallback mechanisms if the rate-limiting store experiences degradation or failure.
- **Multi-Tenant Granularity:** Support configurable rate limits by API Key, User ID, IP address, Client Tier, and Route/Endpoint.
- **Distributed Consistency:** Ensure accurate global counting across multiple distributed gateway nodes using Redis Cluster and atomic Lua execution.
- **Standardized Headers:** Adhere to IETF rate-limit header standards (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`).
## 3. Scope and Exclusions
- **In Scope:**
    - API Gateway middleware integration (e.g., Envoy, Kong, or custom gateway middleware).
    - Distributed Redis-backed Sliding Window Counter and Token Bucket algorithms.
    - Multi-tier quota management (e.g., Tier 1: Build, Tier 2: Launch, Tier 3: Grow / Custom).
    - Standardized response headers and `429 Too Many Requests` error payload.
    - Metrics, logging, and tracing integration (Prometheus, OpenTelemetry).
- **Exclusions:**
    - Client-side rate-limit retry SDK implementation (handled by standard HTTP client exponential backoff and retry policies).
    - Long-term billing and monetization reporting (the rate limiter handles real-time runtime throttling; billing metrics are processed asynchronously via Kafka event streams).
## 4. Detailed Workflows and Diagrams
### Request Flow Architecture
1. **Request Interception:** The client sends an HTTP request containing authentication credentials (API Key or Bearer Token) to the API Gateway.
2. **Context Resolution:** The gateway extracts routing and identity metadata (Tenant ID, Client Tier, Route ID).
3. **Atomic Evaluation:** The gateway executes an atomic Lua script against the Redis Cluster to evaluate the current rate limit window and increment counters or consume tokens.
4. **Outcome Routing:**
    - **Within Quota:** The request proceeds to downstream microservices, with current rate-limit telemetry appended to response headers.
    - **Exceeded Quota:** The request is short-circuited at the gateway level, returning a `429 Too Many Requests` status code.
## 5. Public Contracts (Signatures, Endpoints, Headers, Examples)
### Response Headers (Successful / Normal Requests)
- `X-RateLimit-Limit`: Maximum allowed requests within the current window (e.g., `1000`).
- `X-RateLimit-Remaining`: Remaining requests left in the current window (e.g., `945`).
- `X-RateLimit-Reset`: Unix timestamp when the rate limit window resets (e.g., `1775955600`).
### Response Headers (Rate Limited Requests)
- `Retry-After`: Number of seconds the client must wait before making a new request (e.g., `30`).
### Internal Control Plane API
- `POST /api/v1/ratelimits/rules`: Create or update rate limit policies per tenant/tier.
- `GET /api/v1/ratelimits/quotas/{client_id}`: Fetch current quota consumption and window state.
## 6. Errors, Exceptions, and Fallback
### Error Response Payload (`429 Too Many Requests`)
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. You have made 1001 requests in the current window. Limit is 1000.",
    "retry_after_seconds": 30,
    "reset_timestamp": 1775955600
  }
}
```
### Fallback Strategy (Fail-Open)

- **Strategy:** **Fail-Open**. If the Redis cluster experiences network partitions, high latency (>5ms timeout), or unresponsiveness, the gateway falls back to allowing requests to pass through while emitting a critical alert. This prioritizes system availability over strict quota enforcement during rare infrastructure outages.
## 7. Observability
### Metrics (Prometheus)
- `ratelimit_requests_total`: Counter categorized by status (`allowed`, `rejected`), tier, and route.
- `ratelimit_latency_seconds`: Histogram measuring Redis evaluation latency and gateway middleware overhead.
- `ratelimit_redis_errors_total`: Counter tracking connection timeouts or Redis execution errors.
### Distributed Tracing (OpenTelemetry)
- Span attributes attached to incoming gateway requests: `ratelimit.status` (`ALLOW` / `DENY`), `ratelimit.tier`, and `ratelimit.remaining`.
### Logging & Alerts
- Structured JSON audit logs for every `429` rejection containing client ID, route hash, and current window state. PagerDuty alert triggered if Redis error rate exceeds 1% over a 5-minute rolling window.
## 8. Dependencies and Compatibility
- **Infrastructure Dependencies:** Redis Cluster (v7.0+) supporting server-side Lua scripting for atomic sliding window operations.
- **Service Dependencies:** Authentication Service / API Gateway Auth Middleware (for identity and tier resolution).
- **Backward Compatibility:** Fully backward compatible; clients unaware of rate-limiting headers process standard HTTP responses and handle standard HTTP status codes (`429`).
## 9. Technical Criteria
- **Performance & Latency:** p99 evaluation latency < 2ms under peak load (10,000 RPS per gateway node).
- **Scalability:** Horizontal scaling of API gateways with shared distributed state in Redis Cluster.
- **Security:** Secure transmission of credentials and robust tenant isolation in rate-limit keys (`ratelimit:{tenant_id}:{route_hash}`).
- **Testability:** Comprehensive unit tests for sliding window algorithms and integration tests simulating Redis partitions and high-concurrency race conditions.
## 10. Risks and Mitigation
- **Risk 1: Redis Hotspotting / Key Contention**
    - _Mitigation:_ Shard Redis keys by hashed client identifiers and route prefixes to distribute load evenly across Redis cluster hash slots.
- **Risk 2: Redis Outage Causing Downstream Outages**
    - _Mitigation:_ Implement strict fail-open policy with circuit breakers and tight timeouts (5ms max timeout on Redis calls).
- **Risk 3: Clock Drift Across Distributed Nodes**
    - _Mitigation:_ Use Redis server-side time (`TIME` command or server-side TTL/timestamp evaluation in Lua scripts) rather than relying on client or gateway local system clocks.

## References
[[System Design]]
