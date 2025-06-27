# FastAPI Redis React Microservice

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ValentineOO_fastapi-redis-react-microservice&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ValentineOO_fastapi-redis-react-microservice) ![Python](https://img.shields.io/badge/python-3.8+-blue?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green?logo=fastapi&logoColor=white) ![React](https://img.shields.io/badge/React-18+-blue?logo=react&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-5.3+-red?logo=redis&logoColor=white)

A modern microservices-based e-commerce application demonstrating event-driven architecture with FastAPI, Redis, and React. This project showcases real-world patterns including asynchronous message processing, inventory management, and inter-service communication.

## 🏗️ Architecture

This application follows a microservices architecture with three main components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  Inventory API  │    │  Payment API    │
│    (React)      │    │   (FastAPI)     │    │   (FastAPI)     │
│                 │    │                 │    │                 │
│ • Product List  │◄──►│ • CRUD Products │    │ • Create Orders │
│ • Order Mgmt    │    │ • Inventory Mgmt│    │ • Process Payments│
│ • User Interface│    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                │    ┌─────────────────┐ │
                                └───►│ Redis Streams   │◄┘
                                     │                 │
                                     │ • Event Queue   │
                                     │ • Data Storage  │
                                     │ • Pub/Sub       │
                                     └─────────────────┘
```

### Services Overview

- **Inventory Service** (`inventory/`): Manages product catalog and stock levels
- **Payment Service** (`payment/`): Handles order processing and payment workflows
- **Frontend UI** (`inventory-ui/`): React-based user interface
- **Redis**: Serves as both database and message broker for inter-service communication

## ✨ Features

- 🔄 **Event-Driven Architecture**: Asynchronous communication using Redis Streams
- 📦 **Inventory Management**: Real-time stock updates and product management
- 💰 **Order Processing**: Complete order lifecycle with automatic fee calculation
- 🔄 **Background Processing**: Async order completion simulation
- 🔒 **Error Handling**: Automatic refund mechanism for failed inventory updates
- 🌐 **CORS-Enabled**: Full frontend-backend integration support
- 🎯 **RESTful APIs**: Clean, well-structured API endpoints

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Redis Server
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://gitlab.com/ValentineOO/fastapi-redis-react-microservice.git
   cd fastapi-redis-react-microservice
   ```

2. **Set up Redis**
   ```bash
   # Using Docker (recommended)
   docker run -d -p 6379:6379 --name redis redis:latest
   
   # Or install locally (Ubuntu/Debian)
   sudo apt-get install redis-server
   redis-server
   ```

3. **Configure Environment Variables**
   
   Create `.env.inventory` in the `inventory/` directory:
   ```env
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_USERNAME=
   REDIS_PASSWORD=
   ```
   
   Create `.env.payment` in the `payment/` directory:
   ```env
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_USERNAME=
   REDIS_PASSWORD=
   PRODUCT_SERVICE_URL=http://localhost:8000
   ```

4. **Start the Inventory Service**
   ```bash
   cd inventory
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Start the Payment Service**
   ```bash
   cd payment
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8001 --reload
   ```

6. **Start Redis Consumers** (in separate terminals)
   ```bash
   # Inventory consumer
   cd inventory
   python consumer.py
   
   # Payment consumer (if exists)
   cd payment
   python consumer.py
   ```

7. **Start the Frontend**
   ```bash
   cd inventory-ui
   npm install
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Inventory API: http://localhost:8000
- Payment API: http://localhost:8001

## 📚 API Documentation

### Inventory Service (Port 8000)

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/products` | List all products | - |
| POST | `/products` | Create a new product | `{"name": str, "price": float, "quantity": int}` |
| GET | `/products/{pk}` | Get specific product | - |
| DELETE | `/products/{pk}` | Delete a product | - |

### Payment Service (Port 8001)

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/orders/{pk}` | Get order details | - |
| POST | `/orders` | Create a new order | `{"id": str, "quantity": int}` |

### Example API Usage

**Create a Product:**
```bash
curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{"name": "Laptop", "price": 999.99, "quantity": 10}'
```

**Place an Order:**
```bash
curl -X POST "http://localhost:8001/orders" \
     -H "Content-Type: application/json" \
     -d '{"id": "product_id_here", "quantity": 2}'
```

## 🔄 Event Flow

1. **Order Creation**: User places order via frontend → Payment service
2. **Product Validation**: Payment service fetches product from Inventory service
3. **Order Processing**: Order saved with "pending" status, background task triggered
4. **Order Completion**: After 5 seconds, order status → "completed"
5. **Event Publishing**: `order_completed` event published to Redis Stream
6. **Inventory Update**: Inventory consumer processes event, updates stock
7. **Error Handling**: If inventory update fails → refund event created

## 🏗️ Data Models

### Product (Inventory Service)
```python
{
    "id": "string",
    "name": "string",
    "price": float,
    "quantity": int
}
```

### Order (Payment Service)
```python
{
    "id": "string",
    "product_id": "string",
    "price": float,
    "fee": float,        # 20% of product price
    "total": float,      # price + fee
    "quantity": int,
    "status": "string"   # pending, completed, refunded
}
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for Python APIs
- **Redis**: In-memory data structure store for caching and messaging
- **Redis-OM**: Object mapping library for Redis
- **Uvicorn**: ASGI server for Python web applications
- **Python-dotenv**: Environment variable management

### Frontend
- **React**: JavaScript library for building user interfaces
- **Create React App**: Toolchain for React development

### Development & Quality
- **SonarQube**: Code quality and security analysis
- **Python typing**: Type hints for better code quality

## 🔧 Development

### Project Structure
```
fastapi-redis-react-microservice/
├── inventory/                 # Inventory microservice
│   ├── main.py               # FastAPI app and routes
│   ├── consumer.py           # Redis stream consumer
│   ├── requirements.txt      # Python dependencies
│   └── .env.inventory        # Environment variables
├── payment/                  # Payment microservice
│   ├── main.py               # FastAPI app and routes
│   ├── consumer.py           # Redis stream consumer
│   ├── requirements.txt      # Python dependencies
│   └── .env.payment          # Environment variables
├── inventory-ui/             # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   └── App.js           # Main app component
│   └── package.json         # Node.js dependencies
└── README.md                # This file
```

### Running Tests
```bash
# Backend tests (when implemented)
cd inventory && python -m pytest
cd payment && python -m pytest

# Frontend tests
cd inventory-ui && npm test
```

### Code Quality
This project uses SonarQube for code quality analysis. The current quality gate status is shown in the badge above.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Valentine OO** - *Initial work* - [ValentineOO](https://gitlab.com/ValentineOO)

## 🙏 Acknowledgments

- FastAPI community for excellent documentation
- Redis team for powerful data structures
- React team for the amazing UI library
- All contributors who helped improve this project

## 📞 Support

If you have any questions or need help:
- Create an [issue](https://gitlab.com/ValentineOO/fastapi-redis-react-microservice/-/issues)
- Check the [documentation](https://gitlab.com/ValentineOO/fastapi-redis-react-microservice)
- Contact the maintainer

---

⭐ Star this repository if you found it helpful!
