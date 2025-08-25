# TripTrek Backend (FastAPI + LangChain + LangGraph)

This backend powers the TripTrek application, providing AI-driven travel planning and itinerary generation. It uses **FastAPI** for the API layer, and leverages **LangChain** and **LangGraph** to orchestrate generative AI workflows for building structured travel content.

---

## 🛠️ Tools & Technologies

- **FastAPI**  
  A modern, high-performance Python web framework for building APIs with automatic OpenAPI docs.

- **LangChain**  
  A framework for developing applications powered by language models. Used here to structure prompts, parse outputs, and manage the flow of AI-generated travel content.

- **LangGraph**  
  An extension of LangChain for building complex, multi-step, and branching workflows with language models.

- **Google Gemini API**  
  Provides the LLM (Large Language Model) used for generating travel itineraries and recommendations.

---

## ⚙️ How It Works

1. **API Endpoint**  
   The main endpoint accepts travel-related parameters (such as destination, interests, duration, etc.).

2. **Itinerary Generation**  
   - The backend uses LangChain prompts and output parsers to instruct the LLM to generate a structured travel itinerary.
   - LangGraph can be used for advanced workflows, such as generating daily plans, recommendations, and summaries.

3. **Output**  
   The endpoint returns a JSON object representing the full itinerary, including destinations, daily plans, activities, recommendations, and summaries.

---

## 📤 Example Output JSON

```json
{
  "success": true,
  "message": "Trip created successfully",
  "data": {
    "trip": {
      "id": "cmek7k0oh0003bqjw6hx0hxcu",
      "title": "Tokyo Adventure - April",
      "description": "A cultural journey to Tokyo",
      "month": "April",
      "status": "planned",
      "userId": "cm8c7d973775efcf9b62c63e8",
      "rawItinerary": "**Day 1: Arrival in Tokyo**\n- **Morning**: Arrive at Haneda Airport, transfer to hotel\n- **Evening**: Walk around Shinjuku and enjoy local dinner\n\n**Day 2: Cultural Tokyo**\n- **Morning**: Visit Meiji Shrine\n- **Afternoon**: Explore Asakusa and Senso-ji Temple\n- **Evening**: Tokyo Skytree view and dinner",
      "weatherForecast": "April in Tokyo: Average High 18°C (64°F), Average Low 10°C (50°F). Expect light rainfall (5 inches/month). Clothing: light jacket, umbrella recommended. Advice for Travelers: cherry blossoms still bloom early April.",
      "foodCultureInfo": "**Ramen Shops**: Affordable and widely available.\n**Sushi Bars**: Fresh, mid-range to high-end options.\n**Izakaya**: Great for casual dining and drinks.\n**Tempura Restaurants**: Moderate pricing, excellent for lunch.",
      "activitySuggestions": "Explore Shinjuku nightlife, try sushi at Tsukiji Market, day trip to Mt. Fuji.",
      "usefulLinks": [
        { "title": "Tokyo Travel Guide", "url": "https://www.japan-guide.com/tokyo" },
        { "title": "JR Pass Info", "url": "https://www.japanrailpass.net" }
      ],
      "destinations": [
        {
          "id": "dest123",
          "name": "Tokyo",
          "country": "Japan",
          "tripId": "cmek7k0oh0003bqjw6hx0hxcu"
        }
      ],
      "itinerary": [
        {
          "id": "it1",
          "dayNumber": 1,
          "dayTitle": "Arrival in Tokyo",
          "tripId": "cmek7k0oh0003bqjw6hx0hxcu",
          "activities": [
            {
              "id": "a1",
              "title": "Arrive at Haneda Airport",
              "description": "Check-in and settle at hotel",
              "timeOfDay": "Morning",
              "category": "sightseeing",
              "itineraryId": "it1"
            },
            {
              "id": "a2",
              "title": "Shinjuku Evening Walk",
              "description": "Explore nightlife and try local izakaya",
              "timeOfDay": "Evening",
              "category": "cultural",
              "itineraryId": "it1"
            }
          ]
        },
        {
          "id": "it2",
          "dayNumber": 2,
          "dayTitle": "Cultural Tokyo",
          "tripId": "cmek7k0oh0003bqjw6hx0hxcu",
          "activities": [
            {
              "id": "a3",
              "title": "Visit Meiji Shrine",
              "description": "Traditional Shinto shrine in Shibuya",
              "timeOfDay": "Morning",
              "category": "cultural",
              "itineraryId": "it2"
            },
            {
              "id": "a4",
              "title": "Tokyo Skytree Dinner",
              "description": "Evening view and dining experience",
              "timeOfDay": "Evening",
              "category": "dining",
              "itineraryId": "it2"
            }
          ]
        }
      ],
      "user": {
        "id": "cm8c7d973775efcf9b62c63e8",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com"
      }
    },
    "generatedData": {
      "hasItinerary": true,
      "hasWeatherInfo": true,
      "hasFoodInfo": true,
      "hasActivitySuggestions": true,
      "usefulLinksCount": 2
    }
  }
}
