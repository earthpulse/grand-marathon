import { env } from '$env/dynamic/private';

export async function load() {
	const api_url = env.API_URL;

	return {
		api_url,
	};
}
