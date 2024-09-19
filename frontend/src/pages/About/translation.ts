export const getTranslatedText = (
	text: string | undefined,
	textUk: string | undefined,
	textEn: string | undefined,
	language: string
): string => {
	if (language === "uk") {
		return textUk || text || "";
	} else {
		return textEn || text || "";
	}
};
