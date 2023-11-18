require('lib.systemd')
require('lib.etc')
require('lib.networking')
require('lib.users')

systemd {
	zramGenerator = {
		zram0 = {
			['zram-size'] = 'ram * 2.5',
			['writeback-device'] = '/dev/disk/by-label/swap',
			['priority'] = 100,
		},
	},
}

systemd {
	services = {
		systemd.makeService {
			name = 'fix-igt-freq',
			wantedBy = 'basic.target',
			description = 'Fix IGPU frequency',
			type = 'oneshot',
			execStart = 'intel_gpu_frequency -c min=500',
		},
	},
}

etc {
	hostName = 'diffusion',
}
