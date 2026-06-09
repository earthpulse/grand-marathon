import { env } from '$env/dynamic/private';

export async function load({ fetch }) {
	const api_url = env.API_URL;

	if (!api_url) {
		return { api_url: null, news: null, alerts: null, actions: null };
	}

	let news = null;
	let alerts = null;
	let actions = null;

	try {
		const [resNews, resAlerts, resActions] = await Promise.all([
			fetch(`${api_url}/news`),
			fetch(`${api_url}/alerts`),
			fetch(`${api_url}/actions`)
		]);

		if (resNews.ok) {
			news = await resNews.json();
		}
		if (resAlerts.ok) {
			alerts = await resAlerts.json();
		}
		if (resActions.ok) {
			actions = await resActions.json();
		}
	} catch (e) {
		console.error('Failed to fetch confirm page data', e);
	}

	return {
		api_url,
		news,
		alerts,
		actions,
	};
}
