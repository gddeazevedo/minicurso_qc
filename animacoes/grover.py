from manim import *
import numpy as np


class GroverAlgorithm(Scene):
    def construct(self):
        n_states = 8
        target = 5
        iterations = 2

        title = Text("Algoritmo de Grover", font_size=42)
        title.to_edge(UP)

        subtitle = MathTex(
            r"\text{Busca por } |5\rangle \text{ em } N=8"
        ).scale(0.8)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle))

        axes = Axes(
            x_range=[-0.5, n_states - 0.5, 1],
            y_range=[-0.5, 1, 0.25],
            x_length=10,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": False},
        )

        axes.shift(DOWN * 0.8)

        state_labels = VGroup()

        for i in range(n_states):
            label = MathTex(rf"|{i}\rangle").scale(0.65)
            label.next_to(axes.c2p(i, 0), DOWN)
            state_labels.add(label)

        self.play(Create(axes), Write(state_labels))

        amplitude = 1 / np.sqrt(n_states)
        amplitudes = np.ones(n_states) * amplitude

        bars = self.create_bars(
            axes,
            amplitudes,
            target
        )

        initial_label = MathTex(
            r"|s\rangle"
            r"="
            r"\frac{1}{\sqrt{8}}"
            r"\sum_{x=0}^{7}|x\rangle"
        ).scale(0.75)

        initial_label.to_corner(UL).shift(DOWN * 1.3)

        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars],
                lag_ratio=0.08
            ),
            Write(initial_label)
        )

        self.wait()

        self.play(
            FadeOut(initial_label)
        )

        for iteration in range(iterations):
            iteration_label = Text(
                f"Iteração de Grover {iteration + 1}",
                font_size=30
            )
            iteration_label.next_to(subtitle, DOWN)

            self.play(FadeIn(iteration_label))

            oracle_label = MathTex(
                r"O_f:\quad"
                r"|x\rangle"
                r"\rightarrow"
                r"(-1)^{f(x)}|x\rangle"
            ).scale(0.75)

            oracle_label.to_corner(UL).shift(DOWN * 1.4)

            oracle_box = SurroundingRectangle(
                bars[target],
                color=YELLOW,
                buff=0.08
            )

            self.play(
                Write(oracle_label),
                Create(oracle_box)
            )

            amplitudes[target] *= -1

            new_bars = self.create_bars(
                axes,
                amplitudes,
                target
            )

            self.play(
                Transform(bars, new_bars),
                Flash(
                    axes.c2p(target, amplitudes[target]),
                    color=YELLOW
                )
            )

            self.wait(0.5)

            mean = np.mean(amplitudes)

            mean_line = DashedLine(
                axes.c2p(-0.4, mean),
                axes.c2p(n_states - 0.6, mean),
                color=BLUE
            )

            mean_label = MathTex(
                r"\bar{a}"
            ).scale(0.7)

            mean_label.next_to(mean_line, RIGHT)

            self.play(
                FadeOut(oracle_label),
                FadeOut(oracle_box),
                Create(mean_line),
                Write(mean_label)
            )

            diffuser_label = MathTex(
                r"D = 2|s\rangle\langle s| - I",
                r"\qquad",
                r"a_i \rightarrow 2\bar{a}-a_i"
            ).scale(0.72)

            diffuser_label.to_corner(UL).shift(DOWN * 1.4)

            self.play(Write(diffuser_label))

            new_amplitudes = 2 * mean - amplitudes

            reflection_lines = VGroup()

            for i in range(n_states):
                start = axes.c2p(i, amplitudes[i])
                end = axes.c2p(i, new_amplitudes[i])

                line = Arrow(
                    start,
                    end,
                    buff=0.03,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.15,
                    color=WHITE
                )

                reflection_lines.add(line)

            self.play(
                LaggedStart(
                    *[GrowArrow(arrow) for arrow in reflection_lines],
                    lag_ratio=0.05
                )
            )

            new_bars = self.create_bars(
                axes,
                new_amplitudes,
                target
            )

            self.play(
                Transform(bars, new_bars),
                FadeOut(reflection_lines)
            )

            amplitudes = new_amplitudes

            self.play(
                FadeOut(mean_line),
                FadeOut(mean_label),
                FadeOut(diffuser_label),
                FadeOut(iteration_label)
            )

            self.wait(0.5)

        final_box = SurroundingRectangle(
            bars[target],
            color=GREEN,
            buff=0.1,
            stroke_width=4
        )

        probability = amplitudes[target] ** 2

        result = MathTex(
            rf"P(5)"
            rf"="
            rf"|\langle 5|\psi\rangle|^2"
            rf"\approx"
            rf"{probability:.2f}"
        ).scale(0.85)

        result.to_corner(UL).shift(DOWN * 1.4)

        success = Text(
            "Estado encontrado!",
            color=GREEN,
            font_size=34
        )

        success.next_to(result, DOWN)

        self.play(
            Create(final_box),
            Write(result),
            FadeIn(success),
            bars[target].animate.set_color(GREEN)
        )

        self.play(
            Flash(
                axes.c2p(target, amplitudes[target]),
                color=GREEN,
                line_length=0.5,
                num_lines=16
            )
        )

        self.wait(3)

    def create_bars(self, axes, amplitudes, target):
        bars = VGroup()

        width = 0.75

        for i, amplitude in enumerate(amplitudes):
            zero = axes.c2p(i, 0)
            point = axes.c2p(i, amplitude)

            height = abs(point[1] - zero[1])

            if height < 0.001:
                height = 0.001

            color = YELLOW if i == target else BLUE

            rectangle = Rectangle(
                width=width,
                height=height,
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=color
            )

            if amplitude >= 0:
                rectangle.move_to(
                    axes.c2p(i, amplitude / 2)
                )
            else:
                rectangle.move_to(
                    axes.c2p(i, amplitude / 2)
                )

            bars.add(rectangle)

        return bars