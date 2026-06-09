import { env } from '$env/dynamic/private';

export async function load({ fetch }) {
	const api_url = env.API_URL

	if (!api_url) {
		return { api_url: null, aoi: null, dates: null };
	}

	let aoi = null;
	let dates = null;
	let alerts = null;
	let actions = null;
	let hotspots = null;
	try {
		const [resAoi, resDates, resAlerts, resActions, resHotspots] = await Promise.all([
			fetch(`${api_url}/aoi`),
			fetch(`${api_url}/dates`),
			fetch(`${api_url}/alerts`),
			fetch(`${api_url}/actions`),
			fetch(`${api_url}/hotspots`),
		]);
		if (resAoi.ok) {
			aoi = await resAoi.json();
		}
		if (resDates.ok) {
			dates = await resDates.json();
		}
		if (resAlerts.ok) {
			alerts = await resAlerts.json();
		}
		if (resActions.ok) {
			actions = await resActions.json();
		}
		if (resHotspots.ok) {
			hotspots = await resHotspots.json();
		}
	} catch (e) {
		console.error('Failed to fetch dashboard data', e);
	}

	return {
		api_url,
		aoi,
		dates,
		alerts,
		actions,
		hotspots,
	};
}
