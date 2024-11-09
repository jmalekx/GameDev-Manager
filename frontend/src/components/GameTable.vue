<template>
    <div>
        <div class="d-flex justify-content-between mb-4">
            <h3 class="text fw-bold">Games</h3>
            <button type="button" class="btn btn-success btn-lg" @click="openAddModal">
                <i class="bi bi-plus-circle me-2"></i> Add New Game
            </button>
        </div>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            <!-- Loop through each game to display it as a card -->
            <div v-for="(game, index) in games" :key="game.id" class="col">
                <div class="card shadow-sm rounded p-3 h-100">
                    <div class="card-body">
                        <!-- Slightly larger title -->
                        <h5 class="card-title text-primary mb-3" style="font-size: 1.25rem; font-weight: 600;">
                            {{ game.title }}
                        </h5>
                        <p class="card-text">{{ game.description }}</p>
                        <p class="card-text"><strong>Release Date:</strong> {{ game.release_date }}</p>
                        <p class="card-text"><strong>Platform:</strong> {{ game.platform_display }}</p>
                        <p class="card-text"><strong>Developers:</strong></p>
                        <ul class="list-unstyled mb-0">
                            <li v-for="(developer, index) in game.developers" :key="index">
                                <span class="text-muted">{{ developer.developer_name }} ({{ developer.role }})</span>
                            </li>
                        </ul>
                    </div>
                    <div class="card-footer text-center">
                        <button 
                            class="btn btn-warning btn-sm rounded-circle me-2"
                            style="color: white;"
                            @click="openEditModal(game)"
                        >
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button 
                            class="btn btn-danger btn-sm rounded-circle" 
                            style="color: white;" 
                            @click="deleteGame(game)"
                        >
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <GameModal 
            :gameToEdit="gameToEdit"
            @fetch-games="$emit('fetch-games')" 
        />
    </div>
</template>

<script>
import GameModal from './GameModal.vue';
import { baseUrl } from '../main.js';

export default {
    components: {
        GameModal,
    },
    props: {
        games: {
            type: Array,
            required: true,
        },
    },
    data() {
        return {
            gameToEdit: null,
        };
    },
    methods: {
        openEditModal(game) {
            this.gameToEdit = game;
            this.$nextTick(() => {
                const modal = new bootstrap.Modal(document.getElementById('GameModal'));
                modal.show();
            });
        },
        openAddModal() {
            this.gameToEdit = null;
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
                        headers: {
                            'Content-Type': 'application/json',
                        },
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
