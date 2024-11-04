<template>
    <div class="modal fade" id="GameModal" tabindex="-1" aria-labelledby="GameModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <!--header-->
                <div class="modal-header">
                    <h5 class="modal-title" id="GameModalLabel">{{ gameToEdit ? 'Edit Game' : 'Add New Game' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <!--vody-->
                <div class="modal-body">
                    <form @submit.prevent="submitForm">
                        <!--title input-->
                        <div class="mb-3">
                            <label for="title" class="form-label">Title</label>
                            <input type="text" id="title" v-model="form.title" class="form-control" required>
                        </div>
                        <!--desc input-->
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea id="description" v-model="form.description" class="form-control" required></textarea>
                        </div>
                        <!--date input-->
                        <div class="mb-3">
                            <label for="release_date" class="form-label">Release Date</label>
                            <input type="date" id="release_date" v-model="form.release_date" class="form-control" required>
                        </div>
                        <!--select platform-->
                        <div class="mb-3">
                            <label for="platform" class="form-label">Platform</label>
                            <select id="platform" v-model="form.platform" class="form-select" required>
                                <option v-for="platform in platformChoices" :key="platform.value" :value="platform.value">
                                    {{ platform.label }}
                                </option>
                            </select>
                        </div>

                        <!--developers-->
                        <div class="mb-3">
                            <label class="form-label">Developers</label>
                            <div v-for="(developer, index) in form.developers" :key="index" class="d-flex mb-2">
                                <!--dev selection-->
                                <select v-model="developer.developer_id" class="form-select me-2" required>
                                    <option v-for="dev in developers" :key="dev.id" :value="dev.id">
                                        {{ dev.name }}
                                    </option>
                                </select>
                                <!--role selection-->
                                <select v-model="developer.role" class="form-select" required>
                                    <option v-for="role in roles" :key="role.value" :value="role.value">
                                        {{ role.label }}
                                    </option>
                                </select>
                                <!--remove button-->
                                <button type="button" class="btn btn-danger btn-sm ms-2" @click="removeDeveloper(index)">
                                    Remove
                                </button>
                            </div>
                            <!--add dev button-->
                            <button type="button" class="btn btn-secondary btn-sm" @click="addDeveloper">
                                Add Developer
                            </button>
                        </div>
                        
                        <!--submit button-->
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

export default { //vue options api usage= data,methods,props
    props: { //receive gameToEdit prop to determine if editing or adding game
        gameToEdit: {
            type: Object,
            default: null,
        },
    },
    data() { 
        return { //arrays for dropdown choices and form data
            developers: [],
            roles: [
                { value: 'Level Designer', label: 'Level Designer' },
                { value: 'Programmer', label: 'Programmer' },
                { value: 'Artist', label: 'Artist' },
                { value: 'Animator', label: 'Animator' },
                { value: 'Sound Designer', label: 'Sound Designer' },
                { value: 'Project Manager', label: 'Project Manager' },
                { value: 'UI/UX Designer', label: 'UI/UX Designer' },
            ],
            platformChoices: [
                { value: 'PC', label: 'Computer/Laptop' },
                { value: 'Console', label: 'Console' },
                { value: 'Mobile', label: 'Android/iOS' },
            ],
            form: {
                title: '',
                description: '',
                release_date: '',
                platform: '',
                developers: [],
            },
        };
    },
    watch: { //watches gameToEdit to populate/reset form if editing or not
        gameToEdit: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.form.title = newVal.title;
                    this.form.description = newVal.description;
                    this.form.release_date = newVal.release_date;
                    this.form.platform = newVal.platform; // Use the stored value for editing
                    this.form.developers = newVal.developers.map(developer => ({
                        developer_id: developer.developer_id || developer.id,
                        role: developer.role,
                    }));
                } else {
                    this.resetForm();
                }
            },
        },
    },
    methods: { //fetch dev options from api
        async fetchDevelopers() {
            const response = await fetch(`${baseUrl}/api/developers/`);
            const data = await response.json();
            this.developers = data.developers; 
        },
        resetForm() { //reset to empty for new game
            this.form = {
                title: '',
                description: '',
                release_date: '',
                platform: '', 
                developers: [],
            };
        },
        addDeveloper() {
            this.form.developers.push({ developer_id: '', role: 'Level Designer' });
        },
        removeDeveloper(index) {
            this.form.developers.splice(index, 1);
        },
        async submitForm() {
            const method = this.gameToEdit ? 'PUT' : 'POST'; // Determine method
            const url = this.gameToEdit 
                ? `${baseUrl}/api/games/${this.gameToEdit.id}/` 
                : `${baseUrl}/api/games/`;

            const dataToSend = {
                title: this.form.title,
                description: this.form.description,
                release_date: this.form.release_date,
                platform: this.form.platform,
                developers: this.form.developers.map(dev => ({
                    developer_id: dev.developer_id,
                    role: dev.role,
                })),
            };

            try {
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(dataToSend),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                this.$emit('fetch-games'); //emit to refresh the game list
                this.resetForm();
                const modalElement = document.getElementById('GameModal');
                const modal = bootstrap.Modal.getInstance(modalElement);
                modal.hide();
            } catch (error) {
                console.error('Error submitting game:', error);
            }
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
                throw new Error('Edit failed');
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
                throw new Error('Add failed');
            }
        },
        closeModal() {
            const modalElement = document.getElementById('GameModal');
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) {
                modal.hide();
            }
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
