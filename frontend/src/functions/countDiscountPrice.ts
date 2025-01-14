

export const countDiscountPrice = (price?: string, discount?: string) => {
    const transformedDicount = discount ? Math.ceil(+discount) : null;

    let newPrice = null

    if(price && transformedDicount){
        newPrice = +price - +price*transformedDicount/100
    }

    return newPrice ? newPrice : 0
}