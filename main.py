import asyncio
import pygame
from scene import *
from config import *

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    active_scene = SceneMenu()
    clock = pygame.time.Clock()

    while active_scene is not None:
        events = pygame.event.get()
        delta_time = clock.tick(FPS) / 1000.0

        active_scene.process_input(events)
        active_scene.update(delta_time)
        active_scene.render(screen)

        active_scene = active_scene.next_scene

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
