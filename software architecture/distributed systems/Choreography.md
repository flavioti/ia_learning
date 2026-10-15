#softwarearchitecture #microservices #eventdriven

Is a decentralized, event-driven approach where services interact autonomously.


[[Producer and Publisher]]
[[Consumer and Subscriber]]
[[Queue and Topic]]
[[Message]]

## Main messaging models

| Model                                | How it Works                                                                                                                                    | Best Used For                                                                                                             |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Point-to-Point ([[Queue]])** 📨    | A producer sends a message to a specific queue. **Only one consumer** pulls and processes that specific message. Once processed, it is deleted. | **Task distribution.** (e.g., sending an invoice email, processing an image upload).                                      |
| **Publish/Subscribe ([[Topic]])** 📢 | A producer publishes a message to a topic. **Multiple consumers** can subscribe to that topic and each receive their own copy of the message.   | **Event-driven architectures.** (e.g., telling the Inventory, Shipping, and Analytics services that an `OrderWasPlaced`). |

## Popular plataforms

[[Apache Kafka]]
[[RabbitMQ]]
[[AmazonSQS]]
