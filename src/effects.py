import math
import random

import pygame


class Particle:
    """
    Representa uma partícula individual de uma animação.

    Cada partícula possui:
    - Posição.
    - Velocidade horizontal e vertical.
    - Cor.
    - Tamanho.
    - Tempo de vida.
    """

    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
    ) -> None:

        self.x = float(x)
        self.y = float(y)

        self.color = color

        # Direção aleatória para a partícula.
        angle = random.uniform(
            0,
            2 * math.pi,
        )

        # Velocidade inicial.
        speed = random.uniform(
            1.5,
            4.2,
        )

        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed

        # Tamanho inicial.
        self.initial_radius = random.randint(
            3,
            6,
        )

        # Tempo de vida em atualizações.
        self.max_life = 24
        self.life = self.max_life

    def update(self) -> None:
        """
        Atualiza a posição e o tempo de vida.
        """

        self.x += self.velocity_x
        self.y += self.velocity_y

        # Simula uma gravidade leve.
        self.velocity_y += 0.12

        self.life -= 1

    def draw(
        self,
        surface: pygame.Surface,
    ) -> None:
        """
        Desenha a partícula, diminuindo sua intensidade
        visual conforme ela se aproxima do fim da vida.
        """

        if self.life <= 0:
            return

        intensidade = self.life / self.max_life

        # Escurece progressivamente a cor.
        cor_atual = tuple(
            int(componente * intensidade)
            for componente in self.color
        )

        # Reduz o tamanho progressivamente.
        raio = max(
            1,
            int(self.initial_radius * intensidade),
        )

        pygame.draw.circle(
            surface,
            cor_atual,
            (
                round(self.x),
                round(self.y),
            ),
            raio,
        )


class ParticleBurst:
    """
    Controla um conjunto de partículas que se espalham
    a partir de um ponto da tela.

    Pode ser usado para indicar um acerto ou erro.
    """

    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        particle_count: int = 18,
    ) -> None:

        self.particles = [
            Particle(
                x,
                y,
                color,
            )
            for _ in range(particle_count)
        ]

    def update(self) -> None:
        """
        Atualiza todas as partículas.
        """

        for particle in self.particles:
            particle.update()

    def draw(
        self,
        surface: pygame.Surface,
    ) -> None:
        """
        Desenha todas as partículas ativas.
        """

        for particle in self.particles:
            particle.draw(surface)

    @property
    def finished(self) -> bool:
        """
        Informa se todas as partículas desapareceram.
        """

        return all(
            particle.life <= 0
            for particle in self.particles
        )
