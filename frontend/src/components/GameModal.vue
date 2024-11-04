<template>
    <div class="modal fade" id="GameModal" tabindex="-1" aria-labelledby="GameModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="GameModalLabel">{{ gameToEdit ? 'Edit Game' : 'Add New Game' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label for="title" class="form-label">Title</label>
                            <input type="text" id="title" v-model="form.title" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea id="description" v-model="form.description" class="form-control" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="release_date" class="form-label">Release Date</label>
                            <input type="date" id="release_date" v-model="form.release_date" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label for="platform" class="form-label">Platform</label>
                            <select id="platform" v-model="form.platform" class="form-select" required>
                                <option value="PC">Computer/Laptop</option>
                                <option value="Console">Console</option>
                                <option value="Mobile">Android/iOS</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="developers" class="form-label">Developers</label>
                            <select multiple v-model="form.developer_ids" class="form-select" required>
                                <option v-for="developer in developers" :key="developer.id" :value="developer.id">
                                    {{ developer.name }}
                                </option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            {{ gameToEdit ? 'Save Changes' : 'Add Game' }}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { baseUrl } from '../main.js';

export default {
    props: {
        gameToEdit: {
            type: Object,
            default: null,
        },
    },
    data() {
        return {
            developers: [], // to hold the list of developers
            form: {
                title: '',
                description: '',
                release_date: '',
                platform: 'PC', // default platform
                developer_ids: [], // array to hold selected developer IDs
            },
        };
    },
    watch: {
        gameToEdit: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.populateForm(newVal);
                } else {
                    this.resetForm();
                }
            },
        },
    },
    methods: {
        async fetchDevelopers() {
            const response = await fetch(`${baseUrl}/api/developers/`);
            const data = await response.json();
            this.developers = data.developers;
        },
        populateForm(game) {
            this.form.title = game.title;
            this.form.description = game.description;
            this.form.release_date = game.release_date;
            this.form.platform = game.platform;
            this.form.developer_ids = game.developers.map(developer => developer.developer_id);
        },
        resetForm() {
            this.form.title = '';
            this.form.description = '';
            this.form.release_date = '';
            this.form.platform = 'PC';
            this.form.developer_ids = [];
        },
        async submitForm() {
            if (this.gameToEdit) {
                await this.editGame();
            } else {
                await this.addGame();
            }
            this.$emit('fetch-games');
            this.resetForm();
            this.closeModal();
        },
        async editGame() {
            const response = await fetch(`${baseUrl}/api/games/${this.gameToEdit.id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...this.form,
                    developer_ids: this.form.developer_ids, // Include developer IDs for editing
                }),
            });
            if (!response.ok) {
                console.error('Error editing game:', await response.text());
            }
        },
        async addGame() {
            const response = await fetch(`${baseUrl}/api/games/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.form),
            });
            if (!response.ok) {
                console.error('Error adding game:', await response.text());
            }
        },
        closeModal() {
            const modal = new bootstrap.Modal(document.getElementById('GameModal'));
            modal.hide();
        },
    },
    mounted() {
        this.fetchDevelopers(); // Fetch developers when the component is mounted
    },
};
</script>

<style scoped>
/* Add your styles here */
</style>
