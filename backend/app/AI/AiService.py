# from app.services.AI.ConversationHandler import ConversationHandler
# from app.services.AI.RAG import RAG
from app.AI.ChatMessage import ChatMessage
from mistralai import Mistral, CompletionEvent
# from app.utils.logger import ai_logger
from app.chess.Chess import Chess
from app.algorithm.minimax import minimax
from pathlib import Path
import numpy as np


class AiService:
    def __init__(self, rag, api_key: str, context_size: int = 3) -> None:
        self.client = Mistral(api_key=api_key)
        self.rag = rag
        self.context_size = context_size
        # self.model="open-mistral-7b"  # 5/10, mais pas assez rédirigé
        # self.model="open-mixtral-8x7b"  # 6/10, mais tjrs en anglais
        # self.model="open-mixtral-8x22b"  # 8/10, pas mal
        # self.model="mistral-large-2402"  # 10/10, Pas malllll !!
        # self.model="devstral-small-latest"
        # self.model = "mistral-medium-latest"
        self.model = "mistral-small-latest"


    def __build_messages(self, board: np.ndarray, move_history: str, max_depth: int, suggest_move: np.ndarray, suggest_move_str: str) -> list[ChatMessage]:
        messages: list[ChatMessage] = []
        file_folder = Path(__file__).parent

        with open(file_folder / "docs" / "opening.txt", "r") as file:
            opening = file.read()
            messages.append({
                "role": "system",
                "content": f"This is the opening strategy for chess:\n{opening}"
            })


        with open(file_folder / "input" / "bot_prompt.txt", "r") as file:
            bot_prompt = file.read()
            messages.append({
                "role": "system",
                "content": bot_prompt
            })

        with open(file_folder / "input" / "user_input.txt", "r") as file:
            user_input = file.read()
            messages.append({
                "role": "user",
                "content": user_input.format(
                    board=board,
                    move_history=move_history,
                    minimax_str=suggest_move_str,
                    minimax_coor=suggest_move
                )
            })

        return messages

    def suggest(self, board: np.ndarray, move_history: np.ndarray, max_depth: int = 3):

        # The board is maybe optional, but the move history is required
        # Convert move history to a string representation
        # Calculate the best move using minimax algorithm
        # Ask the AI utility of the last move and explain the minimax decision

        minimax_result = minimax(board, move_history, max_depth=max_depth)

        conversation: list[ChatMessage] = self.__build_messages(board=board, move_history=move_history, max_depth=str(minimax_result), suggest_move=minimax_result[:2], suggest_move_str="e4")

        print(conversation)
        return []

        try:
            response_stream = self.client.chat.stream(
                model=self.model,
                messages=conversation
            )
            response = ""

            if hasattr(response_stream, '__iter__'):
                for event in response_stream:
                    if isinstance(event, CompletionEvent):
                        delta = event.data.choices[0].delta
                        if delta and delta.content:
                            token = delta.content
                            response += token
                            yield token

                # ai_logger.info(f"New interaction:\nAsk: {conversation[-1].get('content', None)}\n\nResponse: {response}")

            else:
                # ai_logger.warning("Stream not iterable, falling back to non-streaming")
                regular_response = self.client.chat.complete(
                    model=self.model,
                    messages=conversation
                )
                content = regular_response.choices[0].message.content
                response = content
                yield content
                # ai_logger.info(f"New interaction:\nAsk: {conversation[-1].get('content', None)}\n\nResponse: {response}")

        except Exception as e:
            # ai_logger.error(f"Error in streaming: {e}")
            try:
                regular_response = self.client.chat.complete(
                    model=self.model,
                    messages=conversation
                )
                content = regular_response.choices[0].message.content
                yield content
                # ai_logger.info(f"Fallback response: {content}")
            except Exception as fallback_error:
                # ai_logger.error(f"Fallback also failed: {fallback_error}")
                yield "<span class='text-red-500'>I'm sorry, I couldn't process your request right now. Please try again in a moment.</span>"


if __name__ == "__main__":
    from load_dotenv import load_dotenv
    from app.chess.ChessPresets import ChessPresets
    load_dotenv()
    import os
    ai_service = AiService(rag=None, api_key=os.getenv("MISTRAL_API_KEY"))

    # apply_move(board, np.array(result[:2], dtype=np.int8), 5)

    # king_value = 6 if (len(move_history) + 1) % 2 == 0 else -6

    # positions = np.where(board == king_value)
    # if len(positions[0]) > 0:
    #     y, x = positions[0][0], positions[1][0]

    #     game_status = np.array([
    #         is_king_in_check(board, x, y),
    #         has_available_moves(board, np.append(move_history, np.expand_dims(result[:2], axis=0), axis=0))
    #     ], dtype=np.int8)

    #     print(move_to_str(board, np.array(result[:2], dtype=np.int8), game_status))

    for bloc in ai_service.suggest(board=ChessPresets.default(), move_history=np.empty((0, 2, 3), dtype=np.int8), max_depth=2):
        print(bloc, end="", flush=True)


# if __name__ == "__main__":
#     from pathlib import Path
#     from app.models.core.RagDataset import RagDataset
#     from app.models.core.ChunkFormat import ChunkFormat
#     import os
#     import dotenv

#     dotenv.load_dotenv()
#     api_key = os.getenv("MISTRAL_API_KEY")

#     # print(api_key)
#     # exit(1)

#     # rag = RAG([
#     #     RagDataset(Path(__file__).parent.parent / "data" / "life-timeline.txt", splitter="paragraphs")
#     # ])

#     data_folder = Path(__file__).parent.parent / "data"

#     rag = RAG(datasets=[
#         RagDataset(path=data_folder / "42cursus.txt", chunkFormat=ChunkFormat(datatype="text", splitter="paragraphs")),
#         RagDataset(path=data_folder / "projects.json", chunkFormat=ChunkFormat(datatype="json")),
#         RagDataset(path=data_folder / "experiences.json", chunkFormat=ChunkFormat(datatype="json")),
#         RagDataset(path=data_folder / "educations.json", chunkFormat=ChunkFormat(datatype="json")),
#         RagDataset(path=data_folder / "skills.json", chunkFormat=ChunkFormat(datatype="json")),
#     ])

#     ai_service = AiService(rag=rag, api_key=api_key)

#     # conversation: list[ChatMessage] = [
#     #     {
#     #         "role": "user",
#     #         "content": "Salut, ça va ?",
#     #         "context": ["Le contexte", "Le contexte"]
#     #     },
#     #     {
#     #         "role": "assistant",
#     #         "content": "Je vais super bien et toi ? Comment puis-je t'aider ?"
#     #     },
#     #     {
#     #         "role": "user",
#     #         "content": "Dis-moi",
#     #         "context": ["Le contexte", "Un autre"]
#     #     },
#     #     {
#     #         "role": "assistant",
#     #         "content": "Oui?"
#     #     }
#     # ]
#     conversation = []

#     conversation = ai_service.enrich(messages=conversation, query="En combien de temps Theo a-t-il terminé le cursus de 42 ?")

#     conversation_handler = ConversationHandler()
#     conversation_build: list[MistralInput] = conversation_handler.build(messages=conversation)

#     print("=" * 40)
#     print("Enriched conversation:")
#     for msg in conversation_build:
#         print(f"{msg['role']}: {msg['content']}")
#     # for bloc in ai_service.ask(messages=conversation):
#     #     print(bloc, end="", flush=True)
