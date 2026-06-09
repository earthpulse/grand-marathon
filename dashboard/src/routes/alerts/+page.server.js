import { env } from '$env/dynamic/private';

export async function load({ fetch }) {
	const api_url = env.API_URL

	if (!api_url) {
		return { api_url: null, news: null };
	}

	let alerts = null;
	try {
		const resalerts = await fetch(`${api_url}/alerts`);
		if (resalerts.ok) {
			alerts = await resalerts.json();
		}
	} catch (e) {
		console.error('Failed to fetch dashboard data', e);
	}

	return {
		api_url,
		alerts,
	};
}
