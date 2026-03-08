# type: ignore

import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.colors as colors
import numpy as np
import matplotlib as mpl

import ofig as of

from matplotlib.typing import ColorType

import logging
from typing import TypeAlias, Any, Self
import math
from numpy.typing import ArrayLike

from typing import Optional, Sequence, Annotated, Callable

from scipy.spatial import ConvexHull, distance  # type: ignore[import-untyped]

from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch

from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # type: ignore[import-untyped] # noqa: E501
from mpl_toolkits.mplot3d.axes3d import Axes3D  # type: ignore[import-untyped]
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d.proj3d import proj_transform  # type: ignore[import-untyped] # noqa: E501

from numpy import ndarray

from matplotlib.patches import Patch
from matplotlib.text import Text
from matplotlib.legend import Legend

Array2D: TypeAlias = Annotated[ndarray, (2, 2)]
Array3D: TypeAlias = Annotated[ndarray, (2, 2, 2)]

Seq2D: TypeAlias = Annotated[Sequence[float], 2]
Seq3D: TypeAlias = Annotated[Sequence[float], 3]

Vec2D = Array2D | Seq2D
Vec3D = Array3D | Seq3D

FILL_CONFIG: dict[str, str | float] = {"alpha": 0.5}
EDGE_CONFIG = {"color": "black", "alpha": 1}
NODE_CONFIG = {"color": "black", "alpha": 0.5}
CONTOUR_CMAP = "viridis"


class DimensionError(ValueError):
    """Raised when the dimension of a figure does not agree
    with the plot.

    When this happens, something is going seriously wrong.
    """
    def __init__(self, expected: str, actual: str):
        """
        Args:
            expected: Dimensions of the plot
            actual: Dimensions of the figure
        """
        super().__init__(f"Dimension mismatch: expected {expected},"
                         f" got {actual}")


def ensure_axes_dimension(axes: Axes | Axes3D,  # type: ignore[no-any-unimported] # noqa: E501
                          dim: int) -> None:
    """Assert if the given axes is of the specified dimension.

    Raises:
        :class:`DimensionError`: if :arg:`dim` does not agree with the
            dimension of :arg:`axes:.`
    """
    dimension_to_name = {2: "rectilinear", 3: "3d"}
    if dim in dimension_to_name:
        if (axes.name != dimension_to_name[dim]):
            raise DimensionError(dimension_to_name[dim], axes.name)
    else:
        of.fig3() if dim == 3 else of.fig2()
        logging.warning(f"The current projection is not `{dim}d`."
                        f"A new {"Axes" if dim == 2 else "Axes3D"}"
                        " is created instead.")


#! Immutable 2-dimensional unit square.
unit_square = np.array(
    [[0, 0],
     [0, 1],
     [1, 0],
     [1, 1]]
)
unit_square.flags.writeable = False


#! Immutable 3-dimensional unit cube. Fancy!
unit_cube = np.array(
    [[0, 0, 0],
     [1, 0, 0],
     [0, 1, 0],
     [0, 0, 1],
     [1, 1, 0],
     [0, 1, 1],
     [1, 0, 1],
     [1, 1, 1],]
)
unit_cube.flags.writeable = False


def view_rotate(h_rotate: float, v_rotate: float) -> None:
    """Rotate the current `Axes3D`.

    @param h_rotate the degree to rotate vertically
    @param v_rotate the degree to rotate horizontally
    """
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    ensure_axes_dimension(ax, 3)
    if (isinstance(ax, Axes3D)):  # Make mypy happy
        ax.view_init(h_rotate, v_rotate)
    else:
        raise Exception("This should not happen."
                        "The exception has been checked.")


def view_axis_pos(pos: Optional[str]) -> None:
    """Position labels and ticks of the current Axes3D.

    Args:
        pos: The position, one of :python:`'lower'`,
            :python:`'upper'`,
            :python:`'default'`,
            :python:`'both'`,
            :python:`'none'`,
            and :python:`None`.
    """
    accepted_values: list[str] = ['lower', 'upper', 'default', 'both', 'none']
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    ensure_axes_dimension(ax, 3)
    match pos:
        case None:
            ax.axis('off')
        case other:
            if other in accepted_values:
                for axis in ax.xaxis, ax.yaxis, ax.zaxis:
                    axis.set_label_position(other)
                    axis.set_ticks_position(other)
            else:
                raise ValueError(f"The input {other} is not one of"
                                 f"{str(accepted_values)}.")


def high_res() -> None:
    """Set figures to render in higher resolution.

    Set runtime configuration ``figure.dpi`` to 200.

    Effect:
        Change runtime configurations.
    """
    pylab.rcParams.update({'figure.dpi': 200})


def low_res() -> None:
    """Set figures to render in the default resolution.

    Set runtime configuration ``figure.dpi`` to 100, the default value.

    Effect:
        Change runtime configurations.
    """
    pylab.rcParams.update({'figure.dpi': 100})


def annotate(title: str,
             xlabel: str,
             ylabel: str,
             zlabel: Optional[str] = None) -> None:
    """Annotate the current figure.

    Set :arg:`title`, :arg:`xlabel`, and :arg:`ylabel` of the current axes.
    Also set runtime configurations that style annotations.

    To reset the parameters, call:
    :python:`matplotlib.rcParams.update(matplotlib.rcParamsDefault)`

    Args:
        title: Title of the figure
        xlabel: Labels for the x axis
        ylabel: Labels for the y axis
        zlabel: Labels for the z axis

    Effect:
        Plot to the current active figure.
        Change runtime configurations.
    """

    axes_label_size: str = "x-large"
    plot_title_size: str = "x-large"

    font = {'legend.fontsize': 'x-large',
            'axes.titlesize': plot_title_size,
            'axes.labelsize': axes_label_size,
            'xtick.labelsize': axes_label_size,
            'ytick.labelsize': axes_label_size,
            'text.usetex': False,
            'font.family': 'Open Sans',
            'axes.titlepad': 15, }

    ax: Axes | Axes3D = plt.gca()  # type: ignore[no-any-unimported]

    pylab.rcParams.update(font)
    ax.set_xlabel(xlabel, fontname='PT Serif')
    ax.set_ylabel(ylabel, fontname='PT Serif')
    if (zlabel is not None):
        ensure_axes_dimension(ax, 3)
        if (isinstance(ax, Axes3D)):
            ax.set_zlabel(zlabel, fontname='PT Serif')
        else:
            raise Exception("This should not happen.")

    my_fig = ax.get_figure()

    if (my_fig is not None):
        my_fig.suptitle(title, fontname='PT Serif')
    else:
        raise Exception("Somehow the Axes is not attached to a Figure. How?")


def heatmap(data: ndarray,
            xlabels: Optional[Sequence[str]] = None,
            ylabels: Optional[Sequence[str]] = None) -> None:
    """Plot a matrix to the current active axis as a heatmap.

    Args:
        data: A Numpy matrix.
        xlabels: labels for cells along the x axis.
        ylabels: labels for cells along the x axis.

    Effects:
        Plot at the current active axis.
    """
    if not isinstance(data, ndarray):
        # If the input is not an numpy array, attempt to cast it into one.
        data = np.array(data)

    # Configure the size of the plot to accommodate the size of each cell
    plt.rcParams["figure.figsize"] = [len(data) * math.sqrt(len(data)),
                                      len(data[0]) * math.sqrt(len(data[0]))]

    xlabels = xlabels if (xlabels is not None)\
        else ["X" + str(i) for i, _ in enumerate(data[0])]
    ylabels = ylabels if (ylabels is not None)\
        else ["Y" + str(i) for i, _ in enumerate(data)]

    ax = plt.gca()

    ensure_axes_dimension(ax, 2)
    ax.imshow(data, cmap="Greys")

    ax.set_xticks(np.arange(len(xlabels)), labels=xlabels)
    ax.set_yticks(np.arange(len(ylabels)), labels=ylabels)

    plt.setp(ax.get_xticklabels(),
             rotation=45,
             ha="right",
             rotation_mode="anchor")

    max_cell_value = data.max()
    min_cell_value = data.min()

    for i in range(len(ylabels)):
        for j in range(len(xlabels)):
            cell_value_scale = max_cell_value - min_cell_value
            ratio = (data[i, j] - min_cell_value) / cell_value_scale
            ax.text(j, i, "{:.2f}".format(data[i, j]),
                    ha="center",
                    va="center",
                    color="w" if ratio > .6 else "k")

    my_fig = ax.get_figure()
    if (my_fig is not None):
        my_fig.tight_layout()  # type: ignore[union-attr]
        # (When called on an `Axes`, ->get_figure(.) always returns a `Figure`)


def chull(shape:
          Annotated[ndarray, (..., 2)] | Annotated[ndarray, (..., 3)]) -> None:
    """Plot a convex hull to the current active axes.

    Detect the shape of points by inspecting the first in the sequence.

    Args:
        shape: A sequence of 2- or 3-dimensional points.

    Effects:
        Plot at the current active axis.
    """
    # The checker only checks if the first element has the correct dimension.
    match len(shape[0]):
        case 2:
            _chull_2d(shape)
        case 3:
            _chull_3d(shape)
        case _:
            raise ValueError("Input must be either 2 or 3")


def _chull_3d(shape: ndarray) -> None:
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    ensure_axes_dimension(ax, 3)

    hull = ConvexHull(shape)
    for s in hull.simplices:
        tri = Poly3DCollection([shape[s]])

        if "alpha" in FILL_CONFIG:
            tri.set_alpha(FILL_CONFIG["alpha"])
        if "color" in FILL_CONFIG:
            tri.set_color(FILL_CONFIG["color"])

        tri.set_edgecolor('none')
        ax.add_collection3d(tri)
        edges = []
        if distance.euclidean(shape[s[0]], shape[s[1]])\
                < distance.euclidean(shape[s[1]], shape[s[2]]):
            edges.append((s[0], s[1]))
            if distance.euclidean(shape[s[1]], shape[s[2]])\
                    < distance.euclidean(shape[s[2]], shape[s[0]]):
                edges.append((s[1], s[2]))
            else:
                edges.append((s[2], s[0]))
        else:
            edges.append((s[1], s[2]))
            if distance.euclidean(shape[s[0]], shape[s[1]]) <\
                    distance.euclidean(shape[s[2]], shape[s[0]]):
                edges.append((s[0], s[1]))
            else:
                edges.append((s[2], s[0]))
        for v0, v1 in edges:
            ax.plot(xs=shape[[v0, v1], 0],
                    ys=shape[[v0, v1], 1],
                    zs=shape[[v0, v1], 2],
                    **EDGE_CONFIG)

    ax.scatter(shape[:, 0],
               shape[:, 1],
               shape[:, 2],
               marker='o',
               **NODE_CONFIG)


def _chull_2d(points: ndarray) -> None:
    ax = plt.gca()
    ensure_axes_dimension(ax, 2)
    hull = ConvexHull(points)
    ax.plot(points[:, 0], points[:, 1], 'o', **NODE_CONFIG)  # type: ignore[arg-type] # noqa: E501
    for simplex in hull.simplices:
        ax.plot(points[simplex, 0],
                points[simplex, 1],
                **EDGE_CONFIG)  # type: ignore[arg-type]

    ax.fill(points[hull.vertices, 0],
            points[hull.vertices, 1],
            lw=2,
            **FILL_CONFIG)


class BigArrow(FancyArrowPatch):
    """An 2- or 3-dimensional arrow.

    :meta private:
    """
    def __init__(self,
                 start: Seq2D | Seq3D,
                 end: Seq2D | Seq3D,
                 *args: Any,
                 **kwargs: Any):
        default_styles = {
            "mutation_scale": 30,
            "arrowstyle": "-|>",
            "linestyle": "--"
        }
        super().__init__((start[0], start[1]),
                         (end[0], end[1]),
                         *args,
                         **(kwargs | default_styles))
        # Note that two copies of `start` and `end` are preserved:
        #   One copy is passed to ->_posA_posB of the parent class; this copy
        #       is used in `draw`.
        #   the other copy is passed to ->start and ->end of this class; this
        #       copt is used in do_3d_projections.
        self.start = start
        self.end = end

    def draw(self: Self, renderer: Any) -> None:
        super().draw(renderer)

    def do_3d_projection(self: Self, renderer: Any = None) -> Any:
        # The reference
        #   https://github.com/matplotlib/matplotlib/blob/v3.8.2/lib/
        #       mpl_toolkits/mplot3d/art3d.py#L998-L1065
        #   appears to return np.min(tzs).
        # Removing it does not seem to change anything. Still, just to be safe.
        if self.axes is None or not isinstance(self.axes, Axes3D):
            raise Exception("Rendered without axes")
        else:
            txs, tys, tzs = proj_transform(*zip(self.start, self.end),
                                           self.axes.M)
            self.set_positions((txs[0], tys[0]), (txs[1], tys[1]))
            return np.min(tzs)


def arrow(start: Seq2D | Seq3D,
          end: Seq2D | Seq3D,
          *args: Any,
          **kwargs: Any) -> None:
    '''Plot an arrow to the current Axes or Axes3D.

    Args:
        start: The starting point of the arrow.
        end: The ending point of the arrow.

    '''
    ax = plt.gca()
    # Type checking `ax` is necessary, since the arrow
    #       class can handle the difference.
    #   Plotting to 2D (projection='rectilinear') Axes calls `draw`.
    #   Plotting to 3D (projection='3d') calls do_3d_projection.
    #   Still, this function might not work for other projections.
    arrow = BigArrow(start, end, *args, **kwargs)
    ax.add_artist(arrow)


def plot(fun: Callable[[float], float],
         x_range: Seq2D,
         density: int = 1000,
         *args: ArrayLike,
         **kwargs: Any) -> None:
    '''Plot a contour map to the current Axes or Axes3D.

    Args:
        fun: The function to plot.
        x_range: A tuple of the beginning and end of the x axis.
        density: the number of points sampled over each axis.
    '''
    ax = plt.gca()
    x_max: float = max(x_range)
    x_min: float = min(x_range)
    xs, ys = _make_ys(fun=fun,
                      x_range=(x_min, x_max),
                      density=density)
    ax.plot(xs, ys, *args, **kwargs)


def _make_zs(fun: Callable[[float, float], float],
             x_range: Seq2D,
             y_range: Seq2D,
             density: int = 100,) -> tuple[ndarray, ndarray, ndarray]:

    x_max: float = max(x_range)
    x_min: float = min(x_range)
    y_max: float = max(y_range)
    y_min: float = min(y_range)

    xs = np.arange(x_min, x_max, step=(x_max - x_min) / density)
    ys = np.arange(y_min, y_max, step=(y_max - y_min) / density)

    xs, ys = np.meshgrid(xs, ys)
    zs = np.vectorize(fun)(xs, ys)

    # This code is for functions that cannot be properly vectorised.
    # zs = np.empty(shape=(len(ys), len(xs)))
    # for i, x in enumerate(xs):
    #     for j, y in enumerate(ys):
    #         zs[j][i] = fun(x, y)

    return (xs, ys, zs)


def contour(fun: Callable[[float, float], float],
            x_range: Seq2D,
            y_range: Seq2D,
            density: int = 100,
            levels: int = 50,
            cmap: str = CONTOUR_CMAP,
            colorbar: bool = True,
            alpha: float = 0.5) -> None:
    '''Plot a contour map to the current Axes or Axes3D.

    Args:
        fun: The function to plot.
        x_range: A tuple of the beginning and end of the x axis.
        y_range: A tuple of the beginning and end of the y axis.
        density: the number of points sampled over each axis.
        levels: The number of contour lines.
        cmap: The colour map used by the contour map.
        colorbar: If True, draw the colour bar.
    '''
    ax = plt.gca()
    xs, ys, zs = _make_zs(fun, x_range, y_range, density)
    ax.set_aspect('equal')  # Very important, otherwise axes use different scales. # noqa: E501
    cs = ax.contour(xs, ys, zs, levels=levels, cmap=cmap,
                    norm=colors.Normalize(vmin=zs.min(),
                                          vmax=zs.max()),
                    alpha=alpha)

    current_figure = ax.get_figure()
    if colorbar and current_figure is not None:
        current_figure.colorbar(cs)


def wireframe(fun:  # type: ignore[no-any-unimported]
              # Reason: I'm not sure which import is causing this.
              Callable[[float, float], float],
              x_range: Seq2D,
              y_range: Seq2D,
              density: int = 100,
              cmap: str = CONTOUR_CMAP,
              alpha: float = 0.9,
              **kwargs: dict[str, Any]) -> Line3DCollection:
    '''Plot a wireframe map to the current Axes or Axes3D.

    Args:
        fun: The function to plot.
        x_range: A tuple of the beginning and end of the x axis.
        y_range: A tuple of the beginning and end of the y axis.
        density: the number of points sampled over each axis.
        cmap: The colour map used by the contour map.
        alpha: Alpha value (transparency) of the frame.
    '''
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    xs, ys, zs = _make_zs(fun, x_range, y_range, density)
    ax.set_aspect('equal')  # Very important, otherwise axes use different scales. # noqa: E501
    return ax.plot_wireframe(xs, ys, zs,
                             cmap=cmap,
                             norm=colors.Normalize(vmin=zs.min(),
                                                   vmax=zs.max()),
                             alpha=alpha,
                             **kwargs)


def surface(fun: Callable[[float, float], float],  # type: ignore[no-any-unimported] # noqa: E501
            x_range: Seq2D,
            y_range: Seq2D,
            density: int = 100,
            cmap: str = CONTOUR_CMAP,
            colorbar: bool = True,
            alpha: float = 0.9) -> Line3DCollection:
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    xs, ys, zs = _make_zs(fun, x_range, y_range, density)
    ax.set_aspect('equal')  # Very important, otherwise axes use different scales. # noqa: E501
    cs = ax.plot_surface(xs, ys, zs,
                         cmap=cmap,
                         norm=colors.Normalize(vmin=zs.min(), vmax=zs.max()),
                         alpha=alpha,
                         rstride=1,
                         cstride=1,
                         edgecolor='none')

    if colorbar:
        ax.get_figure().colorbar(cs)
    return cs


def _make_ys(fun: Callable[[float], float],
             x_range: Seq2D,
             density: int = 20) -> tuple[Array2D, Array2D]:
    x_max: float = max(x_range)
    x_min: float = min(x_range)
    xs = np.linspace(x_min, x_max, num=density, dtype=np.float64)
    ys = np.array([fun(x) for x in xs])
    return xs, ys


def splatter(fun: Callable[[float], float],
             x_range: Seq2D,
             density: int = 30,
             plot_links: bool = False,
             *,
             edge_args: dict[str, Any] = {},
             node_args: dict[str, Any] = {},
             fill_args: dict[str, Any] = {}) -> None:

    xs, ys = _make_ys(fun, x_range, density)

    shatter(xs=xs,
            ys=ys,
            plot_links=plot_links)


def shatter(xs: Vec2D, ys: Vec2D,
            plot_links: bool = False,
            *,
            edge_config: dict[str, Any] = {},
            node_config: dict[str, Any] = {},
            fill_config: dict[str, Any] = {}) -> None:

    edge_args: dict[str, Any] = EDGE_CONFIG | edge_config
    # The default node style now borrows from edge style.
    node_args: dict[str, Any] = node_config
    fill_args: dict[str, Any] = FILL_CONFIG | fill_config

    ax = plt.gca()

    # Incorporate alpha into edge color. Because `->scatter(.)` does not allow
    #   alpha to be specified for `edgecolors`, this is necessary.
    edge_color: Optional[ColorType] = edge_args.get("color")
    edge_alpha: Optional[float] = edge_args.get("alpha")
    if edge_color is not None and edge_alpha is not None:
        line_color = mpl.colors.colorConverter.to_rgba(
            edge_color,
            edge_alpha
        )

    old_x = old_y = None

    if (plot_links):
        ax.plot((min(xs), max(xs)), (0, 0),
                color=line_color,
                linewidth=1,
                zorder=-1)

    for (x, y) in zip(xs, ys):
        ax.plot([x, x], [0, y],
                zorder=0,
                linewidth=1,
                **edge_args)

        if (plot_links):
            if old_x is not None and old_y is not None:
                #Hull it
                ax.plot((old_x, x), (old_y, y), color="#696969", linewidth=0.5,
                        zorder=-1)
                ax.fill_between((old_x, x), (old_y, y),
                                zorder=-2,
                                color="#F5F5F5", **fill_args)
        old_x = x
        old_y = y
    ax.scatter(xs, ys, zorder=4,
               facecolor=fill_args.get("color", "white"),
               edgecolors=line_color,
               linewidth=1.5,
               **node_args)


def _add_patch_to_current_legend(patch: Patch, label: str) -> None:
    ax = plt.gca()
    legend = [c for c in ax.get_children() if isinstance(c, Legend)][0]

    handles = legend.legend_handles
    labels = legend.texts

    handles.append(patch)
    labels.append(Text(0, 0, label))

    plt.legend(handles)


def patch(facecolor: ColorType,
          label: str,
          alpha: float = 1,
          width: float = 1,
          height: float = 0.8) -> None:
    new_patch = Patch(facecolor=facecolor,
                      edgecolor=facecolor,
                      label=label,
                      alpha=alpha)

    if plt.gca().get_legend() is None:
        plt.gca().legend(handles=[new_patch],
                         handlelength=width,
                         handleheight=height,
                         loc="lower left")
    else:
        _add_patch_to_current_legend(Patch(facecolor=facecolor,
                                           edgecolor=facecolor,
                                           label=label,
                                           alpha=alpha),
                                     label=label)
