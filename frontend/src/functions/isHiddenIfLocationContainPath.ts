export const isHiddenIfLocationContainPath = (path: string, forbiddenPath: string): boolean => {

    return path.split('/').includes(forbiddenPath)
}