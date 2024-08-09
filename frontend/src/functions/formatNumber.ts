
export const formatNumber = (number: number | string, digistsAfterComma: number | undefined = 2): string => {
    const formatter = new Intl.NumberFormat("uk-UA", {
        style: "decimal",
        minimumFractionDigits: digistsAfterComma,
        maximumFractionDigits: 2,
      });

    return formatter.format(+number)
}