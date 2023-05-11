import matplotlib.pyplot as plot
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import AutoMinorLocator
import matplotlib.pylab as pylab
import numpy
import matplotlib
from mtsssigner.utils.cff_analysis_utils import get_max_d_proportion

# figure, ax = plot.subplots(subplot_kw={"projection": "3d"})

# # Make data.
# X = numpy.arange(0, 30, 1, dtype=int)
# Y = numpy.arange(0, 30, 1, dtype=int)
# X, Y = numpy.meshgrid(X, Y)
# Z = numpy.floor((Y-1)/(X-1))

# # Create colormap

# cmap = pylab.cm.coolwarm  # define the colormap
# # extract all colors from the .jet map
# cmaplist = [cmap(i) for i in range(cmap.N)]
# # force the first color entry to be grey
# cmaplist[0] = (.5, .5, .5, 1.0)

# # create the new map
# cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
#     'Custom cmap', cmaplist, cmap.N)

# # define the bins and normalize
# bounds = numpy.linspace(0, 20, 21)
# norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

# # Plot the surface.
# surface = ax.plot_surface(X, Y, Z, cmap=cmap,
#                        linewidth=0, antialiased=True, norm=norm)

# ax.set_title('Relação entre parâmetros q, k e d')

# # ax.xaxis.set_minor_locator(AutoMinorLocator(5))
# # ax.yaxis.set_minor_locator(AutoMinorLocator(5))
# # ax.zaxis.set_minor_locator(AutoMinorLocator(5))

# # Customize the z axis.
# ax.set_zlim(0, 30)
# ax.zaxis.set_major_locator(LinearLocator(numticks=7))
# # A StrMethodFormatter is used automatically
# ax.zaxis.set_major_formatter('{x:.0f}')
# ax.set(
#     xlabel='x = nº de testes (k)',
#     ylabel='y = nº de blocos (q)',
#     zlabel='z = nº de erros (d)',
# )

# # Add a color bar which maps values to colors.
# figure.colorbar(surface, shrink=0.5, aspect=5)

# # plot.grid(which='minor')
# plot.show()

# proportions = list()
# k = 2
# for q in range(2,260):
#     if not is_prime_power(q):
#         proportions.append(0)
#     d = get_d(q, k)
#     t = q**k
#     proportion = d/t
#     proportions.append(proportion)

# fig, ax = plot.subplots()
# ax.plot(proportions)

# # Shorthand is also supported and curly braces are optional
# fig.tight_layout()
# plot.show()

print(get_max_d_proportion())
