package response

import "time"

// App represents the response json in App endpoints
type App struct {
	ID        string    `json:"id"`
	Type      string    `json:"type"`
	State     AppState  `json:"state"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// AppState represents key/value state data
type AppState map[string]any
