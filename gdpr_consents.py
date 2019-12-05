import pygame
import checkbox
from input_text import InputBox


def gdpr_concents():
    pygame.init()
    screen = pygame.display.set_mode ((300, 325))

    p_cb = checkbox.Checkbox(screen, 20, 150, caption='Consent to collect telemetry', text_offset=(120,1))
    
    clock = pygame.time.Clock()
    input_name = InputBox(130, 118, w=10, h=18)
    input_boxes = [input_name]
    done = False

    board  = pygame.Surface (screen.get_size())
    board  = board.convert()
    board.fill ((250, 250, 250))

    global running
    running = True
    
    def pclick():
        global running
        running = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            # input-text
            for box in input_boxes:
                box.handle_event(event)
            # input-checkbox
            p_cb.update_checkbox(event)

        for box in input_boxes:
            box.update()

        board.fill((250, 250, 250))
        # screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(board)

        text_to_screen(board, 'GDPR compliance', 55, 10, size=32)
        text_to_screen(board, 'Player name:', 20, 120, size=22, color=(0,0,0))
        button(board, 'Continue',130,290,30,30,pclick)

        screen.blit(board, (0, 0))
        p_cb.render_checkbox()
        pygame.display.flip()
        clock.tick(30)

    # print(p_cb.is_checked(), input_name.text)
    return (input_name.text, p_cb.is_checked())


# declare our support functions
def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'data/fonts/orecrusherexpand.ttf'):
    try:

        text = str(text)
        font = pygame.font.Font(None, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e

def button(board, msg, x, y, w, h, action=None):
    def text_objects(text, font):
        black = (0,0,0)
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        # pygame.draw.rect(board, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    #     pygame.draw.rect(board, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    board.blit(textSurf, textRect)

if __name__ == "__main__":
    gdpr_concents()