# ============================================================
# VISIONTALK PROMPT BUILDER
# ============================================================

def build_prompt(
    question,
    chat_history=None,
    image_description=""
):

    print("\n" + "=" * 60)
    print("STEP 7 : BUILDING VISIONTALK PROMPT")
    print("=" * 60)


    # --------------------------------------------------------
    # Conversation history
    # --------------------------------------------------------

    conversation = ""

    if chat_history:

        for message in chat_history:

            role = message.get("role", "")
            content = message.get("content", "")

            conversation += (
                f"{role.capitalize()}: {content}\n"
            )


    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are VisionTalk, a helpful AI assistant designed
to help visually impaired users understand images.

Your job is to answer the user's question about the
uploaded image.

Use the image information and conversation history
provided below.

IMAGE DESCRIPTION:
{image_description}

CONVERSATION HISTORY:
{conversation}

CURRENT USER QUESTION:
{question}

IMPORTANT INSTRUCTIONS:

1. Answer the user's question clearly.
2. Use simple and easy-to-understand language.
3. Focus on information visible in the image.
4. Do not invent information.
5. If something cannot be determined from the image,
   clearly say that it cannot be determined.
6. Keep answers concise and useful for a visually
   impaired user.
7. If the user asks a follow-up question, use the
   previous conversation to understand the question.

ANSWER:
"""

    print("\nPrompt Created Successfully!")

    print("\nPrompt Preview:\n")

    print(prompt[:1500])

    return prompt