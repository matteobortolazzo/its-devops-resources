# PokeBattle

A web app that allows two pokemons to battle each other based on their stats.
It is a simplified version of a pokemon battle system.

The goal is to replace Pokemon AIs with more advanced strategies in the future.
It should not have random factors to prevent luck from influencing the outcome and AI training.

Each pokemon has the following stats:
- HP (Hit Points)
- Attack
- Defense
- Speed
- Type (e.g., Fire, Water, Grass)

The battle system works as follows:
1. Each pokemon takes turns attacking each other.
2. The damage dealt is calculated based on the attacker's Attack stat and the defender's Defense stat.
3. The battle continues until one pokemon's HP reaches zero.
4. Types have advantages and disadvantages (e.g., Fire is strong against Grass but weak against Water).
5. The pokemon with the higher Speed stat attacks first.

## Database

The app uses a PostgreSQL database to store pokemon data.

### Tables
 
- `pokemons`: Stores pokemon stats (id, name, hp, attack, defense, speed, type).
- `battles`: Stores battle records (id, pokemon_a_id, pokemon_b_id, winner_id, created_at).
- `logs`: Stores battle logs (id, battle_id, turn_number, attacker_id, defender_id, damage_dealt).

## Technologies Used

- API: Minimal NET9
- Database: PostgreSQL
- ORM: Entity Framework Core
- Frontend: Angular
- Containerization: Docker
- CI/CD: GitHub Actions

## UI 

The frontend is built using Angular and provides a simple interface to select two pokemons and initiate a battle.

More specifically, the UI allows users to:
- Select two pokemons from a list.
- View the stats of the selected pokemons.
- Start a battle and watch the turn-by-turn log of the battle.
- View the final outcome of the battle.

## Running the App

To run the app using Docker Compose, follow these steps:
1. Ensure you have Docker and Docker Compose installed on your machine.
2. Clone the repository to your local machine.
3. Navigate to the project directory.
4. Run the following command to start the services:
    ```bash
    docker-compose up --build
    ```
5. The API will be accessible at `http://localhost:5000` and the frontend at `http://localhost:4200`.
6. The PostgreSQL database will be running on `localhost:5432`.
7. Use the frontend to select pokemons and start battles.
