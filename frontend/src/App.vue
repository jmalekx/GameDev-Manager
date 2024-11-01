<template>
    <div class="container pt-4">
        <div class="text-center mb-4">
            <h1 class="display-4">
                API Client
            </h1>
        </div>

        <!-- Tabs -->
        <ul class="nav nav-tabs mb-4" id="modelTabs" role="tablist">
            <li class="nav-item">
                <button class="nav-link active" id="developers-tab" data-bs-toggle="tab" data-bs-target="#developers"
                    type="button" role="tab" aria-controls="developers" aria-selected="true" @click="fetchDevelopers">
                    Developers
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="games-tab" data-bs-toggle="tab" data-bs-target="#games" type="button"
                    role="tab" aria-controls="games" aria-selected="false" @click="fetchGames">
                    Games
                </button>
            </li>
        </ul>

        <div class="tab-content" id="modelTabContent">
            <!-- Developer Tab -->
            <div class="tab-pane fade show active" id="developers" role="tabpanel" aria-labelledby="developers-tab">
                <div class="d-flex justify-content-between mb-3">
                    <h3>
                        Developer List
                    </h3>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#DeveloperModal">
                        Add New Developer
                    </button>
                </div>
                <ul class="list-group">
                    <li class="list-group-item d-flex justify-content-between align-items-center"
                        v-for="developer in developers" :key="developer.id">
                        <div>
                            <strong>{{ developer.name }}</strong> - {{ developer.experience_years }} years
                        </div>
                        <div>
                            <button class="btn btn-sm btn-warning me-2">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger">
                                Delete
                            </button>
                        </div>
                    </li>
                </ul>
            </div>

            <!-- Game Tab -->
            <div class="tab-pane fade" id="games" role="tabpanel" aria-labelledby="games-tab">
                <div class="d-flex justify-content-between mb-3">
                    <h3>
                        Games List
                    </h3>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#GameModal">
                        Add New Game
                    </button>
                </div>
                <ul class="list-group">
                    <li class="list-group-item d-flex justify-content-between align-items-center" v-for="game in games"
                        :key="game.id">
                        <div>
                            <strong>{{ game.title }}</strong> - {{ game.platform }}
                        </div>
                        <div>
                            <button class="btn btn-sm btn-warning me-2">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger">
                                Delete
                            </button>
                        </div>
                    </li>
                </ul>
            </div>

             <!-- Developer Modal -->
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal fade" id="DeveloperModal" tabindex="-1" aria-labelledby="AddDeveloper" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="AddDeveloper">Add Developer</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                ...
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                    Close
                                </button>
                                <button type="button" class="btn btn-primary">
                                    Save changes
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            developers: [],
            games: [],
            modalType: 'Developer', // Tracks whether modal is for Developer or Game
            editMode: false,
            formData: {},
        };
    },
    methods: {
        async fetchDevelopers() {
            const response = await fetch('http://localhost:8000/api/developers.json');
            const data = await response.json();
            this.developers = data.developers;
        },
        async fetchGames() {
            const response = await fetch('http://localhost:8000/api/games.json');
            const data = await response.json();
            this.games = data.games;
        },
    },
    mounted() {
        this.fetchDevelopers(); // Fetch developers on initial load
    }
};
</script>