-- bootstrap lazy.nvim, LazyVim and your plugins
-- check if its vscode if then return

if vim.g.vscode then
  -- running on vscode! goodbye.
  return
end

require("config.lazy")
