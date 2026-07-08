/**
 * Markdown 渲染工具
 * 用于 Day11 智能体对话中 AI 回复的 Markdown 渲染
 */
import MarkdownIt from "markdown-it";

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  breaks: true,
});

export function renderMarkdown(text) {
  if (!text) return "";
  return md.render(text);
}

export default md;
