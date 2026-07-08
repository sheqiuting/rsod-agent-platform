/**
 * 智能体对话状态管理
 * 管理对话会话列表、当前会话消息等
 */
import { defineStore } from "pinia";

export const useAgentStore = defineStore("agent", {
  state: () => ({
    currentSessionId: null,
    messages: [],
    sessions: [],
    isLoading: false,
    abortController: null,
  }),
  getters: {
    messageCount: (state) => state.messages.length,
    hasSession: (state) => state.sessions.length > 0,
  },
  actions: {
    addMessage(message) {
      this.messages.push(message);
    },
    updateLastAssistantMessage(content) {
      const last = this.messages[this.messages.length - 1];
      if (last && last.role === "assistant") {
        last.content = content;
      }
    },
    setLoading(loading) {
      this.isLoading = loading;
    },
    abort() {
      if (this.abortController) {
        this.abortController();
        this.abortController = null;
        this.isLoading = false;
      }
    },
    newChat() {
      this.currentSessionId = null;
      this.messages = [];
      this.abort();
    },
    clear() {
      this.currentSessionId = null;
      this.messages = [];
      this.sessions = [];
      this.abort();
    },
  },
});
