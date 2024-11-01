<template>
    <div>
        <div class="d-flex justify-content-between mb-3">
            <h3>Developer List</h3>
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#DeveloperModal">
                Add New Developer
            </button>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Experience</th>
                    <th scope="col">Availability</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(developer, index) in developers" :key="developer.id">
                    <th scope="row">{{ index + 1 }}</th>
                    <td>{{ developer.name }}</td>
                    <td>
                        <span class="badge bg-secondary">
                            {{ developer.experience_years }} years
                        </span>
                    </td>
                    <td>
                        <span class="badge" :class="developer.available_to_hire ? 'bg-available' : 'bg-unavailable'">
                            {{ developer.available_to_hire ? 'Yes' : 'No' }}
                        </span>
                    </td>
                    <td>
                        <button 
                            class="btn btn-sm btn me-2"
                            style="background-color: gold; color: white;"
                            @click="editDeveloper(developer)"
                        >
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button 
                            class="btn btn-sm btn"
                            style="background-color: crimson; color: white;" 
                            @click="deleteDeveloper(developer)"
                        >
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <DeveloperModal @fetch-developers="$emit('fetch-developers')" />
    </div>
</template>

<script>
import DeveloperModal from './DeveloperModal.vue';
import { baseUrl } from '../main.js';

export default {
    components: {
        DeveloperModal,
    },
    props: {
        developers: {
            type: Array,
            required: true,
        },
    },
    methods: {
        editDeveloper(developer) {
            this.$emit('show-developer-modal', developer);
            alert('Edit developer - not implemented');
        },
        async deleteDeveloper(developer) {
        if (confirm(`Are you sure you want to delete developer '${developer.name}'?`)) {
            try {
                const response = await fetch(`${baseUrl}/api/developers/${developer.id}/`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: developer.id }),
                });

                if (response.ok) {
                    // Successfully deleted the developer
                    alert(`Developer '${developer.name}' has been deleted.`);
                    // Emit an event to refresh the developer list
                    this.$emit('fetch-developers');
                } else {
                    // Handle error response
                    const errorData = await response.json();
                    alert(`Error deleting developer: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Error deleting developer:', error);
                alert('An error occurred while trying to delete the developer.');
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
    .bg-available {
        background-color: #a8e6cf;
        color: #333;
    }
    .bg-unavailable {
        background-color: #ffabab; 
        color: #333; 
    }
</style>
