// helpers/haptic.js
export const useHaptic = () => {
    // Проверяем, что мы внутри Telegram и API доступно
    const tg = window.Telegram?.WebApp;
    const haptic = tg?.HapticFeedback;

    const light = () => haptic?.impactOccurred('medium');
    const success = () => haptic?.notificationOccurred('success');
    const error = () => haptic?.notificationOccurred('error');

    return { light, success, error };
};