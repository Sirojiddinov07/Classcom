async function createMedia(topicId, mediaItems) {
    if (!topicId) {
        throw new Error("topic_id is required");
    }

    const response = await fetch(`/api/topics/${topicId}`);
    if (!response.ok) {
        if (response.status === 404) {
            throw new Error("Topic not found");
        }
        throw new Error("Failed to fetch topic");
    }

    const topic = await response.json();
    if (!topic.media_creatable) {
        throw new Error("Media creation is not allowed for this topic");
    }

    const formData = new FormData();
    mediaItems.forEach((item, index) => {
        if (!item.file) {
            throw new Error(`File is required for media item ${index}`);
        }
        formData.append(`file[${index}]`, item.file);
        formData.append(`desc[${index}]`, item.desc || item.file.name);
    });

    const mediaResponse = await fetch(`/api/media`, {
        method: 'POST',
        body: formData,
    });

    if (!mediaResponse.ok) {
        const errorData = await mediaResponse.json();
        throw new Error(errorData.error || "Failed to create media");
    }

    return await mediaResponse.json();
}