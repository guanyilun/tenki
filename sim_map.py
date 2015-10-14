import numpy as np, argparse
from enlib import enmap, curvedsky, lensing, powspec
parser = argparse.ArgumentParser()
parser.add_argument("template")
parser.add_argument("powspec")
parser.add_argument("ofile")
parser.add_argument("-L", "--lensed", action="store_true")
parser.add_argument("-g", "--geometry", type=str, default="curved")
parser.add_argument("-l", "--lmax",     type=int, default=0)
parser.add_argument("-s", "--seed",     type=int, default=None)
parser.add_argument("--ncomp",          type=int, default=3)
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()

imap = enmap.read_map(args.template)
lmax = args.lmax or None
shape, wcs = (args.ncomp,)+imap.shape[-2:], imap.wcs
if args.seed is not None: np.random.seed(args.seed)

if args.lensed:
	ps_cmb, ps_phi = powspec.read_camb_scalar(args.powspec)
	if args.geometry == "curved":
		m, = lensing.rand_map(shape, wcs, ps_cmb, ps_phi, lmax=lmax, seed=args.seed, verbose=args.verbosity)
	else:
		u = enmap.rand_map(shape, wcs, ps_cmb)
		phi = enmap.rand_map(shape[-2:], wcs, ps_phi)
		m = lensing.lens_map_flat(u, phi)
else:
	ps = powspec.read_spectrum(args.powspec)
	if args.geometry == "curved":
		m = curvedsky.rand_map(shape, wcs, ps, lmax=lmax, seed=args.seed)
	else:
		m = enmap.rand_map(shape, wcs, ps)

enmap.write_map(args.ofile, m)