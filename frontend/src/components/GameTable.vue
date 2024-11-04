<template>
    <div>
        <div class="d-flex justify-content-between mb-3">
            <h3>Game List</h3>
            <button type="button" class="btn btn-primary" @click="openModal(null)">
                Add New Game
            </button>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Title</th>
                    <th scope="col">Release Date</th>
                    <th scope="col">Platform</th>
                    <th scope="col">Developers</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(game, index) in games" :key="game.id">
                    <th scope="row">{{ index + 1 }}</th>
                    <td>{{ game.title }}</td>
                    <td>{{ game.release_date }}</td>
                    <td>{{ game.platform }}</td>
                    <td>
                        <ul>
                            <li v-for="(developer, index) in game.developers" :key="index">
                                {{ developer.developer_name }} ({{ developer.role }})
                            </li>
                        </ul>
                    </td>
                    <td>
                        <button class="btn btn-sm me-2" style="background-color: gold; color: white;" @click="openModal(game)">
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button class="btn btn-sm" style="background-color: crimson; color: white;" @click="deleteGame(game)">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <GameModal :gameToEdit="gameToEdit" @fetch-games="$emit('fetch-games')" />
    </div>
</template>

<script>
import GameModal from './GameModal.vue';
import { baseUrl } from '../main.js';

export default {
    components: { GameModal },
    props: { games: { type: Array, required: true } },
    data() {
        return { gameToEdit: null };
    },
    methods: {
        openModal(game) {
            this.gameToEdit = game;
            this.$nextTick(() => {
                const modal = new bootstrap.Modal(document.getElementById('GameModal'));
                modal.show();
            });
        },
        async deleteGame(game) {
            if (confirm(`Are you sure you want to delete game '${game.title}'?`)) {
                try {
                    const response = await fetch(`${baseUrl}/api/games/${game.id}/`, {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' },
                    });

                    if (response.ok) {
                        this.$emit('fetch-games');
                    } else {
                        const errorData = await response.json();
                        alert(`Error deleting game: ${errorData.error}`);
                    }
                } catch (error) {
                    console.error('Error deleting game:', error);
                    alert('An error occurred while trying to delete the game.');
                }
            }
        },
    },
};
</script>

<style scoped>
    td, th {
        vertical-align: middle;
    }
    th {
        font-size: 1.25rem;
        padding: 1rem;
        text-align: left;
    }
    ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
</style>
