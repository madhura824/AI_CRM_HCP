import { useDispatch, useSelector } from "react-redux";
import { addUserMessage, updateFromAI, setChatInput } from "../redux/interactionSlice";
import { RootState } from "../redux/store";

export default function ChatPanel() {
  const dispatch = useDispatch();

  const input = useSelector(
    (state: RootState) => state.interaction.chatInput
  );

  const { chat, form } = useSelector(
    (state: RootState) => state.interaction
  );

  const sendMessage = async (msg?: string) => {
    const text = msg || input;
    if (!text.trim()) return;

    //  add user message to chat
    dispatch(addUserMessage(text));

    // 2. clear input
    dispatch(setChatInput(""));

    //call backend
    const res = await fetch("http://127.0.0.1:8000/agent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input_text: text,
        form_state: form,
      }),
    });

    const data = await res.json();

    // update the form details
    console.log("FULL RESPONSE:", data);
    dispatch(updateFromAI(data));
  };

  return (
    <div className="flex flex-col h-full">

      {/* chat box */}
      <div className="flex-1 overflow-auto space-y-3 p-4 bg-gray-50 rounded-lg">

        {chat.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg max-w-[80%] text-sm ${
              msg.role === "user"
                ? "bg-blue-600 text-white ml-auto"
                : "bg-white border"
            }`}
          >
            {msg.text}
          </div>
        ))}

      </div>

      {/* input */}
      <div className="flex gap-2 mt-3">

        <input
          className="flex-1 border rounded-lg p-2"
          value={input}
          onChange={(e) =>
            dispatch(setChatInput(e.target.value))
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
          placeholder="Type your message..."
        />

        <button
          onClick={() => sendMessage()}
          className="bg-blue-600 text-white px-4 rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
}