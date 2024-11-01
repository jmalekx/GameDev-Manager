<template>
    <div class="modal fade" id="DeveloperModal" tabindex="-1" aria-labelledby="DeveloperModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="DeveloperModalLabel">{{ isEditing ? 'Edit Developer' : 'Add New Developer' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" v-model="developer.name" class="form-control" id="name" required />
                        </div>
                        <div class="mb-3">
                            <label for="about" class="form-label">About</label>
                            <textarea v-model="developer.about" class="form-control" id="about"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="experience_years" class="form-label">Experience (Years)</label>
                            <input type="number" v-model="developer.experience_years" class="form-control" id="experience_years" required />
                        </div>
                        <div class="mb-3">
                            <label for="available_to_hire" class="form-label">Available to Hire</label>
                            <select v-model="developer.available_to_hire" class="form-select" id="available_to_hire" required>
                                <option :value="true">Yes</option>
                                <option :value="false">No</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="join_date" class="form-label">Join Date</label>
                            <input type="date" v-model="developer.join_date" class="form-control" id="join_date" required />
                        </div>
                        <button type="submit" class="btn btn-primary">{{ isEditing ? 'Update Developer' : 'Add Developer' }}</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { baseUrl } from '../main.js';

export default {
    data() {
        return {
            developer: {
                name: '',
                about: '',
                experience_years: '',
                available_to_hire: true,
                join_date: ''
            },
            isEditing: false,
        };
    },
    props: {
        developerToEdit: {
            type: Object,
            default: null,
        }
    },
    watch: {
        developerToEdit: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.isEditing = true;
                    this.developer = { ...newVal }; //deep clone to avoid mutation
                } else {
                    this.isEditing = false;
                    this.resetForm(); //reset the form for new developer
                }
            }
        }
    },
    methods: {
        resetForm() {
            this.developer = {
                name: '',
                about: '',
                experience_years: '',
                available_to_hire: true,
                join_date: ''
            };
        },
        async submitForm() {
            const url = this.isEditing 
                ? `${baseUrl}/api/developers/${this.developer.id}/` 
                : `${baseUrl}/api/developers/`;
            const method = this.isEditing ? 'PUT' : 'POST';

            const dataToSend = { 
                name: this.developer.name,
                about: this.developer.about,
                experience_years: this.developer.experience_years,
                available_to_hire: this.developer.available_to_hire,
                join_date: this.developer.join_date
            };

            try {
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dataToSend),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const developerData = await response.json();
                console.log(developerData);

                //emit to refresh the list of developers
                this.$emit('fetch-developers');

                this.resetForm();
                
                const modalElement = document.getElementById('DeveloperModal');
                const modal = bootstrap.Modal.getInstance(modalElement);
                modal.hide();

            } catch (error) {
                console.error('Error updating developer:', error);
            }
        }

    }

};
</script>

<style scoped>
.modal-body {
    padding: 20px;
}
</style>
