from google import genai

client = genai.Client(api_key="PASTE_YOUR_API_KEY")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain Bitcoin in one short sentence."
    )
    print("\n✅ Gemini Response:")
    print(response.text)
except Exception as e:
    print("\n❌ Gemini Error:")
    print(e)
