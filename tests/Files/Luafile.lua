local global = _G
local api    = global.api

local Module = module(...)

Module.Test = function()
  return 'test'
end

return Module
