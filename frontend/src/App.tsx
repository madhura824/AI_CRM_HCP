import FormPanel from "./Components/FormPanel";
import ChatPanel from "./Components/ChatPanel";

function App() {
  return (
    <div className="h-screen flex bg-gray-100">
      
      {/* LEFT PANEL */}
      <div className="w-1/2 border-r bg-white p-6 overflow-auto">
        <h1 className="text-xl font-semibold mb-4">
          Interaction Form
        </h1>
        <FormPanel />
      </div>

      {/* RIGHT PANEL */}
      <div className="w-1/2 p-6 flex flex-col">
        <h1 className="text-xl font-semibold mb-4">
          AI Assistant
        </h1>
        <ChatPanel />
      </div>

    </div>
  );
}

export default App;