def get_fashion_roast(image):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        
        prompt = f"""

            You're here to roast this outfit, Nairobi-style. Stay in character and adjust your tone to match the roast level.

            Guidelines:
            - Be funny, real, hurtful and extremly petty 😏
            - Drop some local slang or vibes (e.g., "hii drip imekataa", "wueh", "uko sure?", "bro achana na gikomba market", "unaeza jaribu LC Waikiki", "mtumba sio luku")
            - Make at least one outrageous fashion prediction or trend 😂
            - Use emojis for spice 🌶️

            Now, look at this fit and drop the verdict. Don’t hold back — unless it’s Light Roast ☕.
            
            """

        
        # Generate content with temperature set to 1.5
        generation_config = genai.types.GenerationConfig(temperature=0.1)
        response = model.generate_content(
            [prompt, image],
            generation_config=generation_config
        )
        return response.text
    
    except Exception as e:
        return f"Error generating roast: {str(e)}"