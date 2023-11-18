---@meta
---@class SystemdConfig
SystemdConfig = {
	---@type { [string]: table }
	services = {},

	---@type { [string]: table }
	zramGenerator = {},
}

---@meta
---@class SystemdService
SystemdService = {
	---@type string
	wantedBy = nil,

	---@type string
	description = nil,

	---@type string
	type = nil,

	---@type string
	execStart = nil,

	---@type string
	name = nil,
}

---@class systemd
systemd = setmetatable({
	---@param customService SystemdService
	---@return function
	makeService = function(customService)
		Hana.assert(customService.name ~= nil, 'the service must have a name.')
		Hana.assert(customService.type ~= nil, 'type must be nonnull')
		Hana.assert(customService.execStart ~= nil, 'execStart must be nonnull')
		Hana.assert(customService.description ~= nil, 'description must be nonnull')
		Hana.assert(customService.wantedBy ~= nil, 'wantedBy must be nonnull.')

		return function()
			local service = {
				Unit = {
					Description = customService.description,
				},

				Install = {
					WantedBy = customService.wantedBy,
				},

				Service = {
					ExecStart = customService.execStart,
					Type = customService.type,
				},
			}

			Hana.writeFile('usr/lib/systemd/system/' .. customService.name .. '.service', Hana.toIni(service))
		end
	end,
}, {
	---@param custom SystemdConfig
	---@return nil
	__call = function(_, custom)
		Hana.makeDirAll('etc/systemd')
		local zram = custom.zramGenerator
		local services = custom.services

		if zram ~= nil then
			Hana.writeFile('etc/systemd/zram-generator.conf', Hana.toIni(zram))
		end

		if services ~= nil then
			Hana.makeDirAll('usr/lib/systemd/system')
			for _, service in pairs(services) do
				service()
			end
		end
	end,
})
