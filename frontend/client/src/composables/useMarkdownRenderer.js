import MarkdownIt from 'markdown-it';

export function useMarkdownRenderer() {
  const md = new MarkdownIt();

  function renderMarkdown(markdownText) {
    return md.render(markdownText);
  }

  return {
    renderMarkdown,
  };
}
