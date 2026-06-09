import { env } from '$env/dynamic/private';

export async function load({ fetch }) {
	const api_url = env.API_URL

	if (!api_url) {
		return { api_url: null, alerts: null, actions: null, predefined: null };
	}

	let alerts = null;
	let actions = null;
	let predefined = null;

	try {
		const [resAlerts, resActions, resPredefined] = await Promise.all([
			fetch(`${api_url}/alerts`),
			fetch(`${api_url}/actions`),
			fetch(`${api_url}/actions/predefined`)
		]);

		if (resAlerts.ok) {
			alerts = await resAlerts.json();
		}
		if (resActions.ok) {
			actions = await resActions.json();
		}
		if (resPredefined.ok) {
			predefined = await resPredefined.json();
		}
	} catch (e) {
		console.error('Failed to fetch act page data', e);
	}

	return {
		api_url,
		alerts,
		actions,
		predefined
	};
}
