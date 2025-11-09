# 🤖 AI Arduino Studio

An intelligent web application that helps you create Arduino projects using natural language and AI assistance.

## ✨ Features

- **Visual Arduino Builder**: Drag and drop components
- **AI-Powered Configuration**: Use natural language to configure sensors and actuators
- **Automatic Code Generation**: Get ready-to-use Arduino (.ino) files
- **Smart Fallback**: Works with or without AI API

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure AI (Optional but Recommended)

**Get Google Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key (it's free to start)

**Set up environment:**
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your Gemini API key and model
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-09-2025
SECRET_KEY=your_secret_key_here
```

**Note:** You can specify any available Gemini model. If not specified, it defaults to `gemini-1.5-flash`.

### 3. Start the Application
```bash
python main.py
```

Visit: http://localhost:5000

## 🧠 AI Capabilities

### With Google Gemini API Key:
- **Intelligent parsing** of natural language instructions
- **Context-aware** component configuration
- **Smart threshold detection** based on real-world scenarios
- **Advanced reasoning** for complex Arduino setups
- **Fast and reliable** Google's Gemini Pro model

**Example prompts:**
- "Turn on LED when it gets dark outside"
- "Activate relay for 5 seconds when motion is detected"
- "Water the plant when soil is too dry"
- "Sound alarm if temperature exceeds 25 degrees"

### Without API Key (Fallback Mode):
- Basic keyword matching
- Simple rule-based configuration
- Still functional for common scenarios

## 🏗️ How It Works

1. **Design**: Add Arduino components (sensors, LEDs, etc.) to your project
2. **Configure**: Type natural language instructions like "turn on LED when dark"
3. **AI Processing**: Gemini analyzes your request and configures component thresholds
4. **Generate**: Download ready-to-use Arduino code
5. **Upload**: Flash the code to your Arduino board

## 📁 Project Structure

```
ai-project-studio/
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── static/             # Frontend assets
│   └── dashboard.html  # Main UI
├── templates/          # HTML templates
│   ├── base.html
│   └── login.html
└── railway.json        # Railway deployment config
```

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required for AI features)
- `SECRET_KEY`: Flask session secret (optional, has default)
- `PORT`: Application port (optional, defaults to 5000)

### Supported Components

**Sensors (Input):**
- Motion Sensor
- Light Sensor  
- Temperature Sensor
- Soil Moisture Sensor
- Button

**Actuators (Output):**
- LED
- Relay
- Servo Motor
- Buzzer

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production (Railway/Heroku)
The app includes production configuration and will automatically use Gunicorn in production environments.

## 💡 Example Usage

1. Add a Motion sensor (pin 2) and LED (pin 13)
2. Type: "Turn on LED for 3 seconds when motion detected"
3. AI configures: Motion threshold=1, LED duration=3 seconds
4. Download generated Arduino code
5. Upload to your Arduino board

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

Open source - feel free to use and modify!