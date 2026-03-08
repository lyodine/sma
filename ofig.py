# type: ignore

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D  # type: ignore[import-untyped]
from typing import Tuple
from typing import Optional
from typing import Any


def fig2(xlims: Optional[Tuple[float, float]] = None,
         ylims: Optional[Tuple[float, float]] = None,
         arg: None | tuple[float, float, float, float] = None,
         **kwargs: Any) -> Tuple[Figure, Axes]:
    """Create then return a figure with a 2-dimensional axis.

    Invoke :meth:`.pyplot.figure` to create figure, then
    invoke :meth:`.pyplot.axes` to create an :class:`Axes`.
    Return both objects in a tuple.

    Args:
        arg: :python:`None` or 4-tuple.

            - :python:`None`: A new full window Axes is added using
              ``subplot(**kwargs)``.

            - 4-tuple of floats *rect* = ``(left, bottom, width, height)``:
              Add a new Axes with dimensions *rect* in normalized
              (0, 1) units, using :meth:`Figure.add_axes` on the current
              figure.

        xlims: Size of figure along the X axis
        ylims: Size of figure along the Y axis
        *args: Positional arguments to pass to :meth:`.pyplot.axes`
        *kwargs: Keyword arguments to pass to :meth:`.pyplot.axes`
    """
    fig = plt.figure()
    ax = plt.axes(arg, projection='rectilinear', **kwargs)
    if (xlims is not None):
        ax.set_xlim(*xlims)
    if (ylims is not None):
        ax.set_ylim(*ylims)
    return (fig, ax)


def fig3(xlims: Optional[Tuple[float, float]] = None,  # type: ignore[no-any-unimported] # noqa: E501
         ylims: Optional[Tuple[float, float]] = None,
         zlims: Optional[Tuple[float, float]] = None,
         arg: None | tuple[float, float, float, float] = None,
         **kwargs: Any) \
        -> Tuple[Figure, Axes3D]:
    """Create then return a figure with a 3-dimensional axis.

    Invoke :meth:`.pyplot.figure` to create figure, then
    invoke :meth:`.pyplot.axes` to create an :class:`Axes3D`.
    Return both objects in a tuple.

    Args:
        arg: :python:`None` or 4-tuple.

            - :python:`None`: A new full window Axes is added using
              ``subplot(**kwargs)``.

            - 4-tuple of floats *rect* = ``(left, bottom, width, height)``:
              Add a new Axes with dimensions *rect* in normalized
              (0, 1) units, using :meth:`Figure.add_axes` on the current
              figure.

        xlims: Size of figure along the X axis
        ylims: Size of figure along the Y axis
        ylims: Size of figure along the Y axis
        *kwargs: Keyword arguments to pass to :meth:`.pyplot.axes`
    """
    fig = plt.figure()
    ax: Axes3D = plt.axes(arg,  # type: ignore[no-any-unimported]
                          projection='3d',
                          **kwargs)

    if (xlims is not None):
        ax.set_xlim(*xlims)
    if (ylims is not None):
        ax.set_ylim(*ylims)
    if (zlims is not None):
        ax.set_zlim(*zlims)
    return (fig, ax)
