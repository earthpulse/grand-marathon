import { env } from '$env/dynamic/private';

export async function load({ fetch }) {
	const api_url = env.API_URL;

	if (!api_url) {
		return { api_url: null, alerts: [], actions: [], dates: { dates: [], today: "" } };
	}

	let alerts = [];
	let actions = [];
	let dates = { dates: [], today: "" };

	try {
		const [resAlerts, resActions, resDates] = await Promise.all([
			fetch(`${api_url}/alerts`),
			fetch(`${api_url}/actions`),
			fetch(`${api_url}/dates`),
		]);

		if (resAlerts.ok) {
			alerts = await resAlerts.json();
		}
		if (resActions.ok) {
			actions = await resActions.json();
		}
		if (resDates.ok) {
			dates = await resDates.json();
		}
	} catch (e) {
		console.error('Failed to fetch report data', e);
	}

	return {
		api_url,
		alerts,
		actions,
		dates,
	};
}
