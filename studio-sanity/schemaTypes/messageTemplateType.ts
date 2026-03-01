import {defineField, defineType} from 'sanity'

export const messageTemplateType = defineType({
  name: 'messageTemplate',
  title: 'Message Template',
  type: 'document',
  fields: [
    defineField({
      name: 'templateType',
      title: 'Template Type',
      type: 'string',
      options: {
        list: [
          {title: 'Introduction', value: 'introduction'},
          {title: 'Follow Up', value: 'follow_up'},
          {title: 'Meeting Request', value: 'meeting_request'},
          {title: 'Thank You', value: 'thank_you'},
          {title: 'Connection Request', value: 'connection_request'},
        ],
      },
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'name',
      title: 'Template Name',
      type: 'string',
      validation: (rule) => rule.required(),
      description: 'Internal name for this template',
    }),
    defineField({
      name: 'content',
      title: 'Template Content',
      type: 'text',
      rows: 6,
      validation: (rule) => rule.required(),
      description: 'Message template with {{variable}} placeholders',
    }),
    defineField({
      name: 'variables',
      title: 'Variables',
      type: 'array',
      of: [{type: 'string'}],
      description: 'Variables used in template (e.g., name, interest, event_name)',
    }),
    defineField({
      name: 'context',
      title: 'Context',
      type: 'object',
      description: 'When to use this template',
      fields: [
        {
          name: 'matchThreshold',
          title: 'Minimum Match Threshold',
          type: 'number',
          description: 'Use for matches above this score (0.0 - 1.0)',
        },
        {
          name: 'eventType',
          title: 'Event Type',
          type: 'string',
          description: 'Specific event type this template is for',
        },
        {
          name: 'tone',
          title: 'Tone',
          type: 'string',
          options: {
            list: [
              {title: 'Professional', value: 'professional'},
              {title: 'Casual', value: 'casual'},
              {title: 'Friendly', value: 'friendly'},
            ],
          },
        },
      ],
    }),
    defineField({
      name: 'exampleOutput',
      title: 'Example Output',
      type: 'text',
      rows: 4,
      description: 'Example of filled-in template (for documentation)',
    }),
  ],
  preview: {
    select: {
      title: 'name',
      subtitle: 'templateType',
    },
  },
})
