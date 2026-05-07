import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface ChatMessage {
  role: "user" | "ai";
  text: string;
}

interface InteractionState {
  form: any;
  followups: any[];
  message: string;
  chat: ChatMessage[];
  chatInput: string;
  artifact_file?: string | null;
}

const initialState: InteractionState = {
  form: {
    hcp_name: "",
    interaction_type: "",
    date: "",
    time: "",
    attendees: [],
    topics_discussed: [],
    materials_shared: [],
    samples_distributed: [],
    sentiment: "",
    outcomes: [],
    followup_actions: [],
  },
  followups: [],
  message: "",
  chat: [],
  chatInput: "",
  artifact_file: null,
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    updateFromAI: (state, action: PayloadAction<any>) => {
      let incomingForm;

  const payload = action.payload;

  if (payload.action === "GENERATE_ARTIFACT") {
    incomingForm = payload.form?.form ?? payload.form;
  } else {
    incomingForm = payload.form;
  }

  if (incomingForm && Object.keys(incomingForm).length > 0) {
    state.form = incomingForm;
  }

  state.followups = Array.isArray(action.payload.ai_suggested_followups)
    ? action.payload.ai_suggested_followups
    : [];

  state.message = action.payload.message || "";

  state.artifact_file =
  action.payload.artifact_file ||
  action.payload.form?.artifact_file ||
  null;

  state.chat.push({
    role: "ai",
    text: action.payload.message,
  });
},

    addUserMessage: (state, action: PayloadAction<string>) => {
      state.chat.push({
        role: "user",
        text: action.payload,
      });
    },

    setChatInput: (state, action: PayloadAction<string>) => {
      state.chatInput = action.payload;
    },
  },
});

export const {
  updateFromAI,
  addUserMessage,
  setChatInput,
} = interactionSlice.actions;

export default interactionSlice.reducer;