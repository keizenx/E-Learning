import json
from pathlib import Path

def generate_postman_collection():
    collection = {
        "info": {
            "name": "École en Ligne API",
            "description": "Collection pour l'API de l'École en Ligne",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": "Authentication",
                "item": [
                    {
                        "name": "Obtain Token",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"username\": \"your_username\",\n\t\"password\": \"your_password\"\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/token/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "token"]
                            }
                        }
                    },
                    {
                        "name": "Refresh Token",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"refresh\": \"your_refresh_token\"\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/token/refresh/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "token", "refresh"]
                            }
                        }
                    },
                    {
                        "name": "Verify Token",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"token\": \"your_access_token\"\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/token/verify/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "token", "verify"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Utilisateurs",
                "item": [
                    {
                        "name": "Liste des utilisateurs",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                }
                            ],
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/utilisateurs/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "utilisateurs"]
                            }
                        }
                    },
                    {
                        "name": "Créer un utilisateur",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                },
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"username\": \"new_user\",\n\t\"email\": \"user@example.com\",\n\t\"password\": \"secure_password\",\n\t\"nom\": \"Nom Utilisateur\",\n\t\"role\": \"STUDENT\"\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/utilisateurs/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "utilisateurs"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Cours",
                "item": [
                    {
                        "name": "Liste des cours",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                }
                            ],
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/cours/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "cours"]
                            }
                        }
                    },
                    {
                        "name": "Créer un cours",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                },
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"titre\": \"Nouveau Cours\",\n\t\"description\": \"Description du cours\",\n\t\"is_active\": true\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/cours/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "cours"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Quiz",
                "item": [
                    {
                        "name": "Liste des quiz",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                }
                            ],
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/quiz/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "quiz"]
                            }
                        }
                    },
                    {
                        "name": "Créer un quiz",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                },
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"titre\": \"Nouveau Quiz\",\n\t\"cours\": \"course_id\",\n\t\"questions\": []\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/quiz/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "quiz"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Forums",
                "item": [
                    {
                        "name": "Liste des forums",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                }
                            ],
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/forums/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "forums"]
                            }
                        }
                    },
                    {
                        "name": "Créer un forum",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                },
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"titre\": \"Nouveau Forum\"\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/forums/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "forums"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Messages",
                "item": [
                    {
                        "name": "Liste des messages",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                }
                            ],
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/messages/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "messages"]
                            }
                        }
                    },
                    {
                        "name": "Envoyer un message",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{access_token}}"
                                },
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n\t\"contenu\": \"Contenu du message\"\n}"
                            },
                            "url": {
                                "raw": "http://127.0.0.1:8000/api/messages/",
                                "protocol": "http",
                                "host": ["127", "0", "0", "1"],
                                "port": "8000",
                                "path": ["api", "messages"]
                            }
                        }
                    }
                ]
            }
        ],
        "variable": [
            {
                "key": "access_token",
                "value": "your_access_token_here"
            }
        ]
    }
    
    # Créer le dossier postman s'il n'existe pas
    output_dir = Path(__file__).parent / "postman"
    output_dir.mkdir(exist_ok=True)
    
    # Sauvegarder la collection
    collection_path = output_dir / "ecole_en_ligne_collection.json"
    with open(collection_path, 'w', encoding='utf-8') as f:
        json.dump(collection, f, ensure_ascii=False, indent=2)
    
    print(f"Collection Postman générée dans : {collection_path}")

if __name__ == "__main__":
    generate_postman_collection() 