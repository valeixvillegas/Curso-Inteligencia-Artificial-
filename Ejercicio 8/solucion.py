import numpy as np
import matplotlib.pyplot as plt
import csv

np.random.seed(42)

# Entorno Cliff Walking 4x12
n_rows, n_cols = 4, 12
start = (3, 0)
goal = (3, 11)
cliff = [(3, c) for c in range(1, 11)]

n_states = n_rows * n_cols
n_actions = 4  # 0: arriba, 1: abajo, 2: izquierda, 3: derecha
Q = np.zeros((n_states, n_actions))

def state_to_index(s):
    return s[0] * n_cols + s[1]

def step(s, a):
    r, c = s
    if a == 0: r = max(0, r - 1)
    elif a == 1: r = min(3, r + 1)
    elif a == 2: c = max(0, c - 1)
    elif a == 3: c = min(11, c + 1)
    s2 = (r, c)
    if s2 in cliff:
        return start, -100, False
    if s2 == goal:
        return s2, -1, True
    return s2, -1, False

# Hiperparametros
alpha = 0.1
gamma = 1.0
epsilon = 0.1
episodes = 500

rewards = []

for ep in range(episodes):
    s = start
    total = 0
    done = False
    while not done:
        si = state_to_index(s)
        if np.random.rand() < epsilon:
            a = np.random.randint(n_actions)
        else:
            a = np.argmax(Q[si])
        s2, r, done = step(s, a)
        si2 = state_to_index(s2)
        Q[si, a] += alpha * (r + gamma * np.max(Q[si2]) * (0 if done else 1) - Q[si, a])
        s = s2
        total += r
    rewards.append(total)

# Evaluacion greedy
s = start
steps = 0
total_r = 0
done = False
path = [s]
while not done and steps < 100:
    a = np.argmax(Q[state_to_index(s)])
    s, r, done = step(s, a)
    path.append(s)
    total_r += r
    steps += 1

print(f"Pasos: {steps}")
print(f"Recompensa: {total_r}")
print(f"Camino: {path}")

# Politica
arrows = ['^', 'v', '<', '>']
print("\nPolitica:")
for r in range(n_rows):
    row = ""
    for c in range(n_cols):
        s_t = (r, c)
        if s_t == start: row += " S "
        elif s_t == goal: row += " G "
        elif s_t in cliff: row += " X "
        else: row += f" {arrows[np.argmax(Q[state_to_index(s_t)])]} "
    print(row)

# Guardar CSV
with open('recompensas.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['episodio', 'recompensa'])
    for i, rew in enumerate(rewards):
        w.writerow([i, rew])

# Grafica con matplotlib
window_size = 10
moving_avg = np.convolve(rewards, np.ones(window_size)/window_size, mode='valid')
plt.figure(figsize=(10, 5))
plt.plot(rewards, alpha=0.3, label='Recompensa cruda por episodio')
plt.plot(range(window_size - 1, len(rewards)), moving_avg, color='red', label='Media movil (10 eps)')
plt.axhline(-13, color='green', linestyle='--', label='Politica optima (-13)')
plt.xlabel('Episodio')
plt.ylabel('Recompensa acumulada')
plt.title('Curva de Entrenamiento Q-learning en Cliff Walking')
plt.legend()
plt.grid(True)
plt.savefig('curva_q_learning.png')
plt.show()