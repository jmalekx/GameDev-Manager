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
                            <label class="form-label">Developers</label>
                            <div v-for="(developer, index) in form.developers" :key="index" class="d-flex mb-2">
                                <select v-model="developer.developer_id" class="form-select me-2" required>
                                    <option v-for="dev in developers" :key="dev.id" :value="dev.id">
                                        {{ dev.name }}
                                    </option>
                                </select>
                                <select v-model="developer.role" class="form-select" required>
                                    <option v-for="role in roles" :key="role.value" :value="role.value">
                                        {{ role.label }}
                                    </option>
                                </select>
                                <button type="button" class="btn btn-danger btn-sm ms-2" @click="removeDeveloper(index)">
                                    Remove
                                </button>
                            </div>
                            <button type="button" class="btn btn-secondary btn-sm" @click="addDeveloper">
                                Add Developer
                            </button>
                        </div>

                        <button type="submit" class="btn btn-primary mt-3">
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
            developers: [], // List of developers fetched from the API
            roles: [
                { value: 'Level Designer', label: 'Level Designer' },
                { value: 'Programmer', label: 'Programmer' },
                { value: 'Artist', label: 'Artist' },
                { value: 'Animator', label: 'Animator' },
                { value: 'Sound Designer', label: 'Sound Designer' },
                { value: 'Project Manager', label: 'Project Manager' },
                { value: 'UI/UX Designer', label: 'UI/UX Designer' },
            ],
            form: {
                title: '',
                description: '',
                release_date: '',
                platform: 'PC',
                developers: [],
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
            this.form.developers = game.developers.map(developer => ({
                developer_id: developer.developer_id,
                role: developer.role,
            }));
        },
        resetForm() {
            this.form.title = '';
            this.form.description = '';
            this.form.release_date = '';
            this.form.platform = 'PC';
            this.form.developers = [];
        },
        addDeveloper() {
            this.form.developers.push({ developer_id: '', role: 'Level Designer' });
        },
        removeDeveloper(index) {
            this.form.developers.splice(index, 1);
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
                body: JSON.stringify(this.form),
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
        this.fetchDevelopers();
    },
};
</script>

<style scoped>
/* Custom styles */
</style>
