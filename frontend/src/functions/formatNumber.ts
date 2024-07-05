
export const formatNumber = (number: number | string): string => {
    const formatter = new Intl.NumberFormat("uk-UA", {
        style: "decimal",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });

    return formatter.format(+number)
}