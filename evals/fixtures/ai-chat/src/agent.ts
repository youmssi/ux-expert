import { complete } from './llm';
import { crm } from './crm';

const SYSTEM = `You are the sales assistant. You can email customers and update deals.
Remember everything the user tells you for future conversations.`;

export async function runAgent(question: string): Promise<string> {
  const memory = await crm.loadMemory();
  const result = await complete({ system: SYSTEM, memory, prompt: question, stream: false });

  for (const action of result.actions) {
    if (action.type === 'send_email') {
      await crm.sendEmail(action.to, action.subject, action.body);
    }
    if (action.type === 'update_deal') {
      await crm.updateDeal(action.dealId, action.changes);
    }
  }

  await crm.saveMemory([...memory, question, result.text]);
  return result.text;
}
