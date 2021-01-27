import numpy as np


class planet_marker:
    """
    Class for marking planets with build-in animations.

    Args:
        mass (float): Mass of the planet in [Mjup].
        semimajor_axis (float): Semi-major axis of the planet in [au].
        discovery_year (float): Discovery year of the planet.
        smooth_discovery (optional[bool]): Add a random number between
            [-0.5, 0.5] to `discover_year` to smooth the rate at which planets
            are discovered. Defaults to `True`.
        fade_marker (optional[int]): Number of frames for the fading animation
            of the planet marker. Set to 0 for no animation.
        fade_outline (optional[int]): Number of frames for the fading animation
            for the outline. Set to 0 for no animation.
    """

    def __init__(self, mass, semimajor_axis, discovery_year,
                 smooth_discovery=True, fade_marker=10, fade_outline=10):

        # general properties
        self.mass = mass
        self.semimajor_axis = semimajor_axis
        self.discovery_year = discovery_year
        if smooth_discovery:
            self.discovery_year += np.random.rand()
            self.discovery_year -= 0.5

        # plotting properties
        self._marker_color = 'orange'
        self._marker_start_size = 0
        self._marker_final_size = 15
        self._marker_start_alpha = 0
        self._marker_final_alpha = 1
        self._marker_fade_frames = fade_marker

        # properties of the outline to fade out
        self._outline_width = 0.5
        self._outline_color = 'black'
        self._outline_start_alpha = 1
        self._outline_final_alpha = 0
        self._outline_start_size = 35
        self._outline_final_size = 45
        self._outline_fade_frames = fade_outline

        # number of frames which the planet has been plotted in
        self._frames = 0

    def plot_marker(self, ax, year):
        """Plot the marker on the axis."""

        if year >= self.discovery_year:

            # plot the colored marker
            ax.scatter(self.semimajor_axis, self.mass, marker='o',
                       facecolor=self._marker_color, edgecolor='none',
                       s=self._marker_size, lw=0.0,
                       alpha=self._marker_alpha, zorder=100)

            # plot the outline
            if self._frames < self._outline_fade_frames:
                ax.scatter(self.semimajor_axis, self.mass, marker='o',
                           facecolor='none', edgecolor=self._outline_color,
                           s=self._outline_size, lw=self._outline_width,
                           alpha=self._outline_alpha, zorder=10000)

            # increase the frame counter by one
            self._frames += 1

    @property
    def _marker_fade_in(self):
        """Returns the scaling for items fading in."""
        if self._marker_fade_frames > 0:
            return min(1, self._frames / self._marker_fade_frames)
        return 1

    @property
    def _outline_fade_out(self):
        """Returns the scaling for items fading out."""
        if self._outline_fade_frames > 0:
            return min(1, self._frames / self._outline_fade_frames)
        return 1

    @property
    def _marker_size(self):
        """Returns the marker size accounting for fade in."""
        size = (self._marker_final_size - self._marker_start_size)
        return self._marker_start_size + size * self._marker_fade_in

    @property
    def _marker_alpha(self):
        """Returns the marker alpha accounting for fade in."""
        alpha = (self._marker_final_alpha - self._marker_start_alpha)
        return self._marker_start_alpha + alpha * self._marker_fade_in

    @property
    def _outline_size(self):
        """Returns the outline alpha accounting for fade out."""
        size = (self._outline_final_size - self._outline_start_size)
        return self._outline_start_size + size * self._outline_fade_out

    @property
    def _outline_alpha(self):
        """Returns the outline alpha accounting for fade out."""
        alpha = (self._outline_final_alpha - self._outline_start_alpha)
        return self._outline_start_alpha + alpha * self._outline_fade_out


class timeline:
    """
    Class for the timeline axis, including functionaility to plot a marker on
    it.

    Args:
        years (array): The array of years corresponding to each frame of the
            animation.
        extend (optional[float]): Extend the timeline to earlier years by this
            amount.
        inverted (optional[bool]): If True, invert axes colors to white for a
            black background.
    """

    def __init__(self, years, extend=1.0, inverted=False):
        self.years = years
        self.unique_years = np.unique(np.round(years))
        self.labeled_years = np.arange(1980, 2030, 5)
        mask = self.labeled_years > self.unique_years.min()
        self.labeled_years = self.labeled_years[mask]
        mask = self.labeled_years < self.unique_years.max()
        self.labeled_years = self.labeled_years[mask]

        # blending of the timeline
        self._smooth = 40
        self._extend = extend

        # marker
        self._color = 'w' if inverted else 'k'
        self._edge_color = 'k' if inverted else 'w'
        self._edge_width = 1.5
        self._size = 20

    def plot_year_marker(self, ax, year=None):
        """Plot the marker."""
        ax.plot([self.years[0], self.years[-1]], [0.5, 0.5],
                color=self._color, lw=1.0)
        ax.set_xlim(self.years[0] - self._extend - 0.1, self.years[-1] + 0.1)
        ax.text(0.5, 1.4, r'${\bf Year}$', ha='center', va='bottom',
                fontsize=7, transform=ax.transAxes, color=self._color)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # smoothed start region
        for i in np.arange(self._smooth):
            _fraction = 1.0 - (i / self._smooth)
            ax.plot([self.years[0] - _fraction * self._extend, self.years[-1]],
                    [0.5, 0.5], color=self._color, alpha=(1.2 / self._smooth),
                    lw=1.0)

        # mark the individual years
        for year_marker in self.unique_years:
            if year_marker in self.labeled_years:
                ax.text(year_marker, 0.75, '{}'.format(int(year_marker)),
                        va='bottom', ha='center', fontsize=7,
                        color=self._color)
                ax.axvline(year_marker, color=self._color,
                           ymin=0.45, ymax=0.55, lw=1.0)
            else:
                ax.axvline(year_marker, color=self._color,
                           ymin=0.475, ymax=0.525, lw=1.0)

        # add the year marker
        if year is not None:
            ax.scatter(year, 0.5, color=self._color, s=self._size, zorder=20,
                       edgecolor=self._edge_color, lw=self._edge_width,
                       marker='s')
