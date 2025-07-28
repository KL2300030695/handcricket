import cv2
import mediapipe as mp
import random
import time

# --- Hand Detection Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils
tip_ids = [4, 8, 12, 16, 20]

# --- Finger Counting Logic ---
def count_fingers(hand_landmarks):
    if hand_landmarks is None:
        return None

    fingers = []

    # Thumb (left vs right hand logic, depends on handedness)
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total = fingers.count(1)
    return 6 if total == 0 else total  # Treat closed fist as 6

# --- Game Variables ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

game_state = "TOSS"
user_score, comp_score, target = 0, 0, -1
inning = 1
user_is_batting = None
feedback = ""
last_move_time = time.time()
move_delay = 2.5

# --- Game Loop ---
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    user_move = None
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        user_move = count_fingers(hand_landmarks)

    current_time = time.time()

    # --- TOSS Stage ---
    if game_state == "TOSS":
        feedback = "TOSS: Show 1 for ODD or 2 for EVEN"
        if user_move in [1, 2] and current_time - last_move_time > move_delay:
            comp_toss = random.randint(1, 6)
            total = user_move + comp_toss
            user_wins_toss = (total % 2 == 0 and user_move == 2) or (total % 2 != 0 and user_move == 1)

            if user_wins_toss:
                feedback = "You won the toss! Show 1 to BAT or 2 to BOWL"
                game_state = "TOSS_CHOICE"
            else:
                comp_choice = random.choice(["BAT", "BOWL"])
                user_is_batting = (comp_choice == "BOWL")
                feedback = f"Computer won toss and chose to {comp_choice}."
                game_state = "PLAYING"
            last_move_time = current_time

    # --- TOSS CHOICE ---
    elif game_state == "TOSS_CHOICE":
        if user_move in [1, 2] and current_time - last_move_time > move_delay:
            user_is_batting = (user_move == 1)
            feedback = "You chose to BAT first!" if user_is_batting else "You chose to BOWL first!"
            game_state = "PLAYING"
            last_move_time = current_time

    # --- PLAYING Stage ---
    elif game_state == "PLAYING":
        if user_move is not None and current_time - last_move_time > move_delay:
            comp_move = random.randint(1, 6)
            last_move_time = current_time

            if user_move == comp_move:
                feedback = f"OUT! You:{user_move} Comp:{comp_move}"
                if inning == 1:
                    target = (user_score if user_is_batting else comp_score) + 1
                    user_is_batting = not user_is_batting
                    inning = 2
                    feedback += f" | Target: {target}"
                else:
                    game_state = "GAME_OVER"
            else:
                if user_is_batting:
                    user_score += user_move
                    feedback = f"You scored {user_move}!"
                    if inning == 2 and user_score >= target:
                        game_state = "GAME_OVER"
                else:
                    comp_score += comp_move
                    feedback = f"Computer scored {comp_move}!"
                    if inning == 2 and comp_score >= target:
                        game_state = "GAME_OVER"

    # --- GAME OVER ---
    elif game_state == "GAME_OVER":
        if user_score > comp_score:
            feedback = "🎉 YOU WON! Press 'R' to Restart"
        elif comp_score > user_score:
            feedback = "😞 COMPUTER WON! Press 'R' to Restart"
        else:
            feedback = "🤝 IT'S A DRAW! Press 'R' to Restart"

        if cv2.waitKey(1) & 0xFF == ord('r'):
            game_state = "TOSS"
            user_score, comp_score, target, inning = 0, 0, -1, 1
            user_is_batting = None
            last_move_time = time.time()
            feedback = ""

    # --- Display ---
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (1280, 100), (0, 0, 0), -1)
    img = cv2.addWeighted(overlay, 0.5, img, 0.5, 0)

    cv2.putText(img, f"YOU: {user_score}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(img, f"COMP: {comp_score}", (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    if target != -1:
        cv2.putText(img, f"TARGET: {target}", (600, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if game_state == "PLAYING":
        player_status = "You are BATTING" if user_is_batting else "You are BOWLING"
        cv2.putText(img, player_status, (900, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    # Feedback line
    cv2.putText(img, feedback, (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Show window
    cv2.imshow("✨ Hand Cricket Game", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
